from fastapi import APIRouter, WebSocket
from starlette.responses import HTMLResponse

from app.sockets.socket_server import sio_server
from pathlib import Path

router = APIRouter(tags=['sockets'])


@router.on_event("shutdown")
async def shutdown_event():
    await sio_server.emit("app_closed", "The application has been closed manually")


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await sio_server.handle_request(websocket)


@router.get("/")
async def get():
    html_path = Path('sockets/page.html').resolve()
    with open(html_path) as f:
        html = f.read()
    return HTMLResponse(html)
