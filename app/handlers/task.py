from fastapi import APIRouter

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get("")
async def get_tasks():
    return [_ for _ in range(10)]


@router.get("/{task_id}")
async def get_task(task_id: int):
    return task_id


@router.put("/{task_id}")
async def update_task(task_id: int):
    return task_id


@router.post("/task")
async def create_task():
    return {
        "task_id": 1
    }
