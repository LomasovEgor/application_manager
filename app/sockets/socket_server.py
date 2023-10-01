import socketio

sio_server = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["*"],
    logger=True
)

sio_app = socketio.ASGIApp(
    socketio_server=sio_server,
)
