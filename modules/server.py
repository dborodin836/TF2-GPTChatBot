import asyncio
from typing import Type, Union, get_type_hints

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError, create_model
from starlette import status
from starlette.responses import Response
from starlette.websockets import WebSocketDisconnect

from config import Config, ValidatableConfig, config
from modules.gui.controller import command_controller
from modules.logs import get_logger
from modules.utils.config import save_config

combo_logger = get_logger("combo")

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
    return create_model("PartialUpdateModel", **field_definitions)  # type: ignore[call-overload]


# Create partial update model dynamically
PartialUpdateModel: Type[BaseModel] = create_partial_update_model(Config)


@app.get("/settings")
async def handle_get_settings():
    return config.dict()


@app.get("/settings/default")
async def handle_get_default_settings():
    # Generate default config
    cfg = Config()
    return cfg.dict()


@app.post("/settings")
async def update_settings(settings: PartialUpdateModel):  # type: ignore[valid-type]
    update_data = {k: v for k, v in settings.dict().items() if v is not None}  # type: ignore[attr-defined]

    try:
        # Get current model as a dict, can't use Config() 'cos of possible session overwrites
        current_config_dict = config.model_dump()
        # Update that dict with data received from request
        current_config_dict.update(update_data)
        # If it doesn't throw ValidationError we're safe to go
        tmp_config = ValidatableConfig(**current_config_dict)
        # Finally replace app config with updated config
        config.update_config(config.model_copy(update=tmp_config.dict(), deep=True))
        # Save config on filesystem
        await asyncio.to_thread(save_config, "config.ini")
    except ValidationError as exc:
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content=exc.json())

    return Response(status_code=status.HTTP_201_CREATED)


@app.post("/cmd")
async def handle_command(command: Command):
    await asyncio.to_thread(command_controller.process_line, command.text)
    return Response(status_code=status.HTTP_200_OK)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
