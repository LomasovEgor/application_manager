from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.programs.dao import ProgramsDAO
from app.programs.manager import ProgramManager
from app.sockets.repeat_every import repeat_every

router = APIRouter(tags=["sockets"])

active_connections_set = set()


@router.get("/")
async def get_index() -> HTMLResponse:
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Chat</title>
</head>
<body>
<h1>Notifications</h1>
<ul id='messages'>
</ul>
<script>
    let ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function (event) {
        let messages = document.getElementById('messages')
        let message = document.createElement('li')
        let content = document.createTextNode(event.data)
        message.appendChild(content)
        messages.appendChild(message)
    };
</script>
</body>
</html>
"""
    return HTMLResponse(html)


async def broadcast(text: str) -> None:
    for websocket in active_connections_set:
        await websocket.send_text(text)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    active_connections_set.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        active_connections_set.remove(websocket)


apps = ProgramManager.get_all_user_processes()


@router.on_event("startup")
async def load_all_programs() -> None:
    for app in apps:
        await ProgramsDAO.add_program_if_not_exist(
            name=app.name, path=str(app.exe_path)
        )


@router.on_event("startup")
@repeat_every(seconds=2)
async def check_processes_task() -> None:
    global apps
    current_apps = ProgramManager.get_all_user_processes()
    closed_apps = [app for app in apps if app not in current_apps]
    for app in closed_apps:
        await broadcast(
            f"The application {app.name} with pid={app.pid} has been closed manually"
        )
    apps = current_apps
    for app in apps:
        await ProgramsDAO.add_program_if_not_exist(
            name=app.name, path=str(app.exe_path)
        )
