from pydantic import BaseModel


class ProgramCreate(BaseModel):
    name: str


class ProgramStatus(BaseModel):
    id: int
    name: str
    status: bool
