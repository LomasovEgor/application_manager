Запуск:
Приложение будет ожидать локально развернутую бд postgres с параметрами:
USER: postgres
PASS: postgres
HOST: localhost
PORT: 5432
DB_NAME: programs
(postgresql+asyncpg://postgres:postgres@localhost:5432/programs)
Сборка:
`python -m nuitka --follow-imports --onefile main.py`

