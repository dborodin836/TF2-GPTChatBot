import asyncio
import threading
from typing import Optional


aio_loop: Optional[asyncio.AbstractEventLoop] = None


async def manage_aio_loop(aio_initiate_shutdown: threading.Event):
    # Communicate the asyncio loop status to tkinter via a global variable.
    global aio_loop
    aio_loop = asyncio.get_running_loop()

    while not aio_initiate_shutdown.is_set():
        await asyncio.sleep(0)


def aio_main(aio_initiate_shutdown: threading.Event):
    asyncio.run(manage_aio_loop(aio_initiate_shutdown))


def get_loop():
    return aio_loop
