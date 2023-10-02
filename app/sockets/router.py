from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.programs.dao import ProgramsDAO
from app.programs.manager import ProgramManager
from app.sockets.repeat_every import repeat_every

router = APIRouter(tags=["sockets"])

active_connections_set = set()


@router.get("/")
async def get_index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Alert Page</title>
</head>
<body>
<h1>Alert Page</h1>
<script>
    let ws = new WebSocket("ws://localhost:8000/ws");
    ws.onmessage = function (event) {
        console.log(event.data)
        alert(event.data)
    };
</script>
</body>
</html>
"""
    return HTMLResponse(html)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections_set.add(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        active_connections_set.remove(websocket)


async def broadcast(text: str):
    for websocket in active_connections_set:
        await websocket.send_text(text)


apps = ProgramManager.get_all_user_processes()


@router.on_event("startup")
async def load_all_programs():
    for app in apps:
        await ProgramsDAO.update_program_status(
            name=app.name, path=str(app.exe_path), new_status=True
        )


@router.on_event("startup")
@repeat_every(seconds=2)
async def check_processes_task():
    global apps
    current_apps = ProgramManager.get_all_user_processes()
    names = [app.name for app in current_apps]
    pids = [app.pid for app in current_apps]
    for app in apps:
        if app.name not in names and app.pid not in pids:
            print(
                f"The application {app.name} with pid={app.pid} has been closed manually"
            )
            await broadcast(
                f"The application {app.name} with pid={app.pid} has been closed manually"
            )
    apps = current_apps
