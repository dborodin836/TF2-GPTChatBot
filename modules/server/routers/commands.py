import asyncio
import copy
import json
from typing import Any, Dict

from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

from modules.builder.utils import create_command_from_dict
from modules.set_once_dict import ModificationOfSetKey
from modules.setup import controller
from modules.typing import Command
from modules.utils.config import save_commands
from modules.utils.schemas import get_compiled_schema

router = APIRouter(
    prefix="/command",
)


@router.get("/schema")
async def handle_command_scheme():
    compiled_schema = await get_compiled_schema("schemas/command.schema.json")
    return Response(status_code=status.HTTP_200_OK, content=json.dumps(compiled_schema))


@router.get("/list")
async def list_commands():
    data = controller.list_commands(custom_only=True)
    dumped = json.dumps(data)
    return Response(status_code=200, content=dumped)


@router.post("/edit/{name}")
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


@router.post("/add")
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


@router.get("/meta/{name}")
async def get_command_meta(name: str):
    try:
        command: Command = controller.get_command(name)
        return Response(status_code=200, content=json.dumps(command.meta))
    except (KeyError, ValueError):
        return Response(status_code=404, content='{"err": "Command not found."}')


@router.post("/delete/{name}")
async def delete_command(name: str):
    try:
        controller.delete_command(name)
        data_to_save = controller.export_commands()
        save_commands(data_to_save)
        return Response(status_code=201)
    except (KeyError, ValueError):
        return Response(status_code=404, content='{"err": "Command not found."}')
