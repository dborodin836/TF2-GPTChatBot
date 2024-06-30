import asyncio
import json

from fastapi import APIRouter, WebSocket
from pydantic import BaseModel
from starlette import status
from starlette.responses import Response
from starlette.websockets import WebSocketDisconnect

from modules.gui.controller import command_controller as gui_cmd_controller
from modules.server.connection_manager import connection_manager
from modules.utils.text import get_stats

router = APIRouter()


class CommandName(BaseModel):
    text: str


@router.post("/cmd")
async def handle_command(command: CommandName):
    await asyncio.to_thread(gui_cmd_controller.process_line, command.text)
    return Response(status_code=status.HTTP_200_OK)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)


@router.get("/stats")
async def stats():
    total_lines_parsed_count, stats_commands_parsed_count, chat_messages_parsed_count = get_stats()
    data = {
        "total_lines_parsed_count": total_lines_parsed_count,
        "stats_commands_parsed_count": stats_commands_parsed_count,
        "chat_messages_parsed_count": chat_messages_parsed_count
    }
    return json.dumps(data)
