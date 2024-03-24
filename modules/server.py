import asyncio
from typing import Type, Union

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, create_model
from pydantic.typing import get_type_hints
from starlette.websockets import WebSocketDisconnect

from config import Config, config, read_config_from_file
from modules.gui.controller import command_controller
from modules.utils.config import save_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


connection_manager = ConnectionManager()


class Command(BaseModel):
    text: str


def create_partial_update_model(base_model: Type[BaseModel]) -> Type[BaseModel]:
    field_definitions = {}
    for name, type_hint in get_type_hints(base_model).items():
        field_definitions[name] = (Union[type_hint, None], None)
    return create_model("PartialUpdateModel", **field_definitions)


# Create partial update model dynamically
PartialUpdateModel = create_partial_update_model(Config)


@app.get("/settings")
async def handle_get_settings():
    return config.dict()


@app.get("/settings/default")
async def handle_get_settings():
    cfg = Config(**read_config_from_file("default.ini"))
    return cfg.dict()


@app.post("/settings")
async def handle_update_settings(settings: PartialUpdateModel):
    update_data = settings.dict()
    errors = []
    success = True

    try:
        for k, v in update_data.items():
            config.__setattr__(k, v)
        save_config("config.ini")
    except Exception as e:
        success = False
        errors.append(str(e))

    response = {"status": "ok" if success else "error"}
    if errors:
        response.update({"errors": errors})

    return response


@app.post("/cmd")
async def handle_command(command: Command):
    await asyncio.to_thread(command_controller.process_line, command.text)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            # Here you can also receive messages
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
