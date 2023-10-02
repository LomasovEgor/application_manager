from pathlib import Path

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["sockets"])

active_connections_set = set()


@router.get("/")
async def get_index():
    with open(Path("app/static/index.html").resolve()) as file:
        html = file.read()
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
        await websocket.close()


# Все варианты ниже не работают. Закрытие соединения websocket происходит до того как выполняется broadcast()
# 1)
@router.on_event("shutdown")
async def on_shutdown():
    await broadcast("The application has been closed manually")


# 2)
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     yield
#     broadcast("The application has been closed manually")

# 3)
# signal.signal(signal.SIGINT, lambda s, f: on_shutdown())

# 4)
# from asyncio import Queue
# message_queue = Queue()
#
# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             message = await message_queue.get()
#             await websocket.send_text(message)
#     except Exception as e:
#         print(f"WebSocket error: {e}")
#     finally:
#         await websocket.close()
#
# async def send_shutdown_message():
#     await message_queue.put("The application has been closed manually")
#
# @app.on_event("shutdown")
# async def on_shutdown():
#     await send_shutdown_message()
