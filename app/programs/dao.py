from app.dao import BaseDAO
from app.programs.models import Program, History


class ProgramsDAO(BaseDAO):
    model = Program

    @classmethod
    async def add_program_if_not_exist(cls, name: str, path: str):
        program = await cls.find_one_or_none(name=name)
        if not program:
            await cls.add(name=name, path=path)

    @classmethod
    async def add_program(cls, name: str, path: str):
        await cls.add(name=name, path=path)

    @classmethod
    async def find_all_programs(cls):
        return await cls.find_all()


class HistoryDAO(BaseDAO):
    model = History

    @classmethod
    async def add_history_record(cls, program_name: str, action: str):
        await cls.add(program_name=program_name, action=action)

    @classmethod
    async def find_all_history(cls):
        return await cls.find_all()
