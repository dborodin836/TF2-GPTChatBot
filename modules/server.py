import asyncio
import copy
import json
from typing import Any, Dict, Type, Union, get_type_hints

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ValidationError, create_model
from starlette import status
from starlette.responses import Response
from starlette.websockets import WebSocketDisconnect

from config import Config, ValidatableConfig, config
from modules.builder.utils import create_command_from_dict
from modules.gui.controller import command_controller as gui_cmd_controller
from modules.logs import get_logger
from modules.set_once_dict import ModificationOfSetKey
from modules.setup import controller
from modules.typing import Command
from modules.utils.config import DROP_KEYS, save_commands, save_config
from modules.utils.schemas import get_compiled_schema

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


class CommandName(BaseModel):
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
    # Remove keys that are useless
    dict_ = {k: v for k, v in cfg.dict().items() if k not in DROP_KEYS}
    return dict_


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
async def handle_command(command: CommandName):
    await asyncio.to_thread(gui_cmd_controller.process_line, command.text)
    return Response(status_code=status.HTTP_200_OK)


@app.get("/schemas/command")
async def handle_command_scheme():
    compiled_schema = await get_compiled_schema("schemas/command.schema.json")
    return Response(status_code=status.HTTP_200_OK, content=json.dumps(compiled_schema))


@app.get("/command/list")
async def list_commands():
    data = controller.list_commands(custom_only=True)
    dumped = json.dumps(data)
    return Response(status_code=200, content=dumped)


@app.post("/command/edit/{name}")
async def edit_command(name: str, command_data: Dict):
    try:
        meta_info_copy = copy.deepcopy(command_data)
        klass = create_command_from_dict(command_data)
        chat_command_name = command_data["prefix"] + command_data["name"]
        controller.delete_command(name)
        await asyncio.to_thread(
            controller.register_command,
            chat_command_name,
            klass.as_command(),
            command_data["name"],
            meta=meta_info_copy,
        )
        data_to_save = controller.export_commands()
        save_commands(data_to_save)
        return Response(status_code=status.HTTP_201_CREATED)
    except Exception:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST, content='{"err": "Error occurred."}'
        )


@app.post("/command/add")
async def add_command(command_data: Dict[Any, Any]):
    try:
        klass = create_command_from_dict(command_data)
        chat_command_name = command_data["prefix"] + command_data["name"]
        await asyncio.to_thread(
            controller.register_command,
            chat_command_name,
            klass.as_command(),
            command_data["name"],
            meta=command_data,
        )
        data_to_save = controller.export_commands()
        save_commands(data_to_save)
        return Response(status_code=status.HTTP_201_CREATED)
    except ModificationOfSetKey:
        return Response(
            status_code=status.HTTP_400_BAD_REQUEST,
            content='{"err": "Command with that name already exist."}',
        )
    except Exception:
        return Response(status_code=500, content='{"err": "Unknown error"}')


@app.get("/command/meta/{name}")
async def get_command_meta(name: str):
    try:
        command: Command = controller.get_command(name)
        return Response(status_code=200, content=json.dumps(command.meta))
    except (KeyError, ValueError):
        return Response(status_code=404, content='{"err": "Command not found."}')


@app.post("/command/delete/{name}")
async def delete_command(name: str):
    try:
        controller.delete_command(name)
        data_to_save = controller.export_commands()
        save_commands(data_to_save)
        return Response(status_code=201)
    except (KeyError, ValueError):
        return Response(status_code=404, content='{"err": "Command not found."}')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
