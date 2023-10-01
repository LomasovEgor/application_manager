from fastapi import APIRouter

router = APIRouter(prefix="/programs", tags=['programs'])


@router.post("/programs/")
def create_program(program):
    pass


@router.get("/programs/")
def read_programs():
    pass


@router.post("/programs/{program_id}/start/")
def start_program(program_id: int):
    pass


@router.post("/programs/{program_id}/stop/")
def stop_program(program_id: int):
    pass


@router.post("/programs/stop_all/", response_model=None)
def stop_all_programs():
    pass
