import uvicorn
from fastapi import FastAPI

from app.programs.router import router as program_router
from app.sockets.router import router as socket_router
from app.sockets.socket_server import sio_app

app = FastAPI()

app.mount("/", sio_app)

app.include_router(program_router)
app.include_router(socket_router)

uvicorn.run(app)
