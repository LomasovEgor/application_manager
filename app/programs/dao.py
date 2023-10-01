from app.dao import BaseDAO
from app.programs.models import Program


class ProgramsDAO(BaseDAO):
    model = Program

