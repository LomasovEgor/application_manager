from pathlib import Path

import psutil
from fastapi import APIRouter

from app.programs.dao import ProgramsDAO, HistoryDAO
from app.programs.manager import ProgramManager

router = APIRouter(prefix="/programs", tags=["programs"])


@router.post("/start")
async def start_program(program_exe_path: str) -> str:
    pid = ProgramManager.run_process(program_exe_path)
    name = Path(program_exe_path).name
    await ProgramsDAO.update_program_status(
        name=name, path=program_exe_path, new_status=True
    )
    await HistoryDAO.add_history_record(name, "start_program")
    return f"Программа {program_exe_path} успешное запущена, {pid=}"


pid = int
info = dict


@router.get("/get_all")
async def get_all_programs() -> dict[pid, info]:
    return ProgramManager.get_all_processes()


@router.post("/stop")
async def stop_program(program_id: int) -> str:
    try:
        gone, alive, name = ProgramManager.kill_proc_tree(program_id)
    except psutil.NoSuchProcess as e:
        return f"Нет процесса с таким pid={e.pid}"
    await HistoryDAO.add_history_record(name, "stop_program")
    await ProgramsDAO.update_program_status(
        name=name, path=name, new_status=False
    )
    return f"Завершенные процессы: {len(gone)}, Живые процессы: {len(alive)}"


@router.post("/stop_all")
async def stop_all_programs() -> str:
    user = ProgramManager.stop_all_user_process()
    return f"Все программы пользователя {user} остановлены"
