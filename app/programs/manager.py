import os
import signal
import subprocess
from pathlib import Path

import psutil

from app.programs.schema import SProgram


class ProgramManager:
    @classmethod
    def run_process(cls, program_path: str):
        process = subprocess.Popen(Path(program_path))
        return process.pid

    @classmethod
    def get_all_user_processes(cls):
        current_user = os.getlogin()
        user_processes = []
        for process in psutil.process_iter(["pid", "name", "username"]):
            if process.info["username"] is not None and process.info[
                "username"
            ].endswith(current_user):
                user_processes.append(
                    SProgram(
                        pid=process.pid,
                        name=process.name(),
                        exe_path=Path(process.exe()),
                        username=process.username(),
                        status="Running",
                    )
                )
        return user_processes

    @classmethod
    def kill_proc_tree(
        cls,
        pid,
        sig=signal.SIGTERM,
        include_parent=True,
        timeout=None,
        on_terminate=None,
    ):
        assert pid != os.getpid()
        parent = psutil.Process(pid)
        name = parent.name()
        children = parent.children(recursive=True)
        if include_parent:
            children.append(parent)
        for p in children:
            try:
                p.send_signal(sig)
            except psutil.NoSuchProcess:
                raise psutil.NoSuchProcess(pid)
        gone, alive = psutil.wait_procs(
            children, timeout=timeout, callback=on_terminate
        )
        return gone, alive, name

    @classmethod
    def stop_all_user_process(cls):
        all_gone = 0
        all_alive = 0
        names = []
        current_user = os.getlogin()
        for process in cls.get_all_user_processes():
            gone, alive, name = cls.kill_proc_tree(process.pid)
            all_gone += gone
            all_alive += alive
            names.append(name)
        return all_gone, all_alive, names, current_user


if __name__ == "__main__":
    print(ProgramManager.get_all_user_processes())
