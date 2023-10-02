from app.dao import BaseDAO
from app.database import async_session_maker
from app.programs.models import Program, History


class ProgramsDAO(BaseDAO):
    model = Program

    @classmethod
    async def update_program_status(cls, name: str, path: str, new_status: bool):
        async with async_session_maker() as session:
            program = await cls.find_one_or_none(name=name)
            if program:
                program.status = new_status
                await session.commit()
            else:
                await cls.add(name=name, path=path, status=new_status)

    @classmethod
    async def add_program(cls, name, path, status):
        await cls.add(name=name, path=path, status=status)

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
