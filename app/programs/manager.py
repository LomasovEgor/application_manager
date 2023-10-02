import os
import signal
import subprocess
from pathlib import Path

import psutil


class ProgramManager:
    @classmethod
    def run_process(cls, program_path: str):
        process = subprocess.Popen(Path(program_path))
        return process.pid

    @classmethod
    def get_all_processes(cls):
        procs = {p.pid: p.info for p in psutil.process_iter(["name", "username"])}
        return procs

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
        current_user = os.getlogin()
        for process in cls.get_all_processes():
            if process.username().endwith(current_user):
                cls.kill_proc_tree(process.ppid())
        return current_user
