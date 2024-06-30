from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import commands, settings, root

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(commands.router)
app.include_router(settings.router)
app.include_router(root.router)
