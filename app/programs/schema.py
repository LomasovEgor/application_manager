from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel


class SProgram(BaseModel):
    pid: int
    name: str
    exe_path: Path
    username: str
    status: Literal["Running", "Not Running"]


class SHistory(BaseModel):
    id: int
    program_name: str
    action: str
    timestamp: datetime


class SKnownProgram(BaseModel):
    id: int
    name: str
    path: str
    status: bool
