from pathlib import Path

import psutil
from fastapi import APIRouter

from app.programs.dao import ProgramsDAO, HistoryDAO
from app.programs.manager import ProgramManager
from app.programs.schema import SProgram, SHistory, SKnownProgram

router = APIRouter(prefix="/programs", tags=["programs"])

pid = int
info = dict


@router.get("/get_all")
async def get_running_programs() -> list[SProgram]:
    """
    Получить все запущенные процессы
    """
    return ProgramManager.get_all_user_processes()


@router.get("/get_all_known")
async def get_known_programs() -> list[SKnownProgram]:
    """
    Содержит программы с известными путями к .exe файлам, удобно для открытия приложений.
    Приложения добавляются в этот список если были запущены хоть один раз
    """
    return await ProgramsDAO.find_all_programs()


@router.post("/start")
async def start_program(program_exe_path: str) -> str:
    pid = ProgramManager.run_process(program_exe_path)
    name = Path(program_exe_path).name
    await ProgramsDAO.add_program_if_not_exist(name=name, path=program_exe_path)
    await HistoryDAO.add_history_record(name, "start_program")
    return f"Программа {program_exe_path} успешное запущена, {pid=}"


@router.post("/stop")
async def stop_program(program_id: int) -> str:
    """
    Закрывает все дерево процессов программы
    """
    try:
        gone, alive, name = ProgramManager.kill_proc_tree(program_id)
    except psutil.NoSuchProcess as e:
        return f"Нет процесса с таким pid={e.pid}"
    await HistoryDAO.add_history_record(name, "stop_program")
    await ProgramsDAO.add_program_if_not_exist(name=name, path=name)
    return f"Завершенные процессы: {len(gone)}, Живые процессы: {len(alive)}"


@router.post("/stop_all")
async def stop_all_programs() -> str:
    user = ProgramManager.stop_all_user_process()
    return f"Все программы пользователя {user} остановлены"


@router.get("/history")
async def get_history() -> list[SHistory]:
    return await HistoryDAO.find_all_history()
