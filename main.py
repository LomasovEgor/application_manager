import subprocess
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from app.programs.router import router as program_router
from app.sockets.router import router as socket_router

app = FastAPI()

app.include_router(program_router)
app.include_router(socket_router)

if __name__ == "__main__":
    try:
        alembic_ini = Path("alembic.ini").resolve()
        subprocess.run(["alembic", "-c", alembic_ini, "upgrade", "head"])
    except Exception as e:
        print(f"An error occurred while running alembic upgrade: {e}")

    uvicorn.run(app)
