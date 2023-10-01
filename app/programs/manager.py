import psutil

import subprocess


# subprocess.Popen(program_path)
#
# # Также можно передавать аргументы командной строки и работать с выводом программы
# output = subprocess.check_output(["dir", "-l"])
# print(output)


class ProgramManager:

    @classmethod
    def run_process(cls, program_path: str):
        # Запустить новую программу
        # program_path = "C:\\Program Files\\Program.exe"
        subprocess.Popen(program_path)
        return subprocess.check_output(["dir", "-l"])

    @classmethod
    def get_all_processes(cls, ):
        procs = {p.pid: p.info for p in psutil.process_iter(['name', 'username'])}
        return procs

    @classmethod
    def stop_process(cls, program_id: int):

        def on_terminate(proc):
            print(f"process {proc} terminated with exit code {proc.returncode}")

        procs = psutil.Process().children()
        process_to_terminate = psutil.Process(program_id)
        process_to_terminate.terminate()

    @classmethod
    def stop_all_user_process(cls, user: str):
        for process in cls.get_all_processes():
            if process.username() == 'DESKTOP-5VO6OCE\\Egorl':
                cls.stop_process(process.ppid())


#
# for process in ProgramManager.get_all_processes():
#     if process.name() == 'Obsidian.exe':
#         ProgramManager.stop_process(process.ppid())

# manager.stop_process(7616)

if __name__ == '__main__':
    print(ProgramManager.get_all_processes())
