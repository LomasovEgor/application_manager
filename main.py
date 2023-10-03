import alembic.command
import uvicorn
from alembic.config import Config
from fastapi import FastAPI

from app.programs.router import router as program_router
from app.sockets.router import router as socket_router

app = FastAPI()

app.include_router(program_router)
app.include_router(socket_router)

if __name__ == "__main__":
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", "migrations")
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/programs?async_fallback=True",
    )

    try:
        alembic.command.upgrade(alembic_cfg, "head")
    except Exception as e:
        print(f"An error occurred while running alembic upgrade: {e}")

    uvicorn.run(app)
