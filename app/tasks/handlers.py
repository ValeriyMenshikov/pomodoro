from fastapi import (
    APIRouter,
    Depends,
)

from app.infrastructure.database import get_repository
from app.tasks.repository.task import TaskRepository
from app.tasks.schema import (
    TaskSchema,
    TasksSchema,
    TaskCreateSchema,
)

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get(
    "",
    # response_model=TasksSchema
)
async def get_tasks(
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
):
    tasks = await task_repository.get_tasks()
    return tasks


@router.get(
    "/{task_id}",
)
async def get_task(
        task_id: int,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
):
    task = await task_repository.get_task(task_id=task_id)
    return task


@router.put(
    "/{task_id}",
    response_model=TaskCreateSchema
)
async def update_task(task: TaskCreateSchema) -> TaskCreateSchema:
    return TaskCreateSchema


@router.post(
    "/task",
    # response_model=TaskCreateSchema
)
async def create_task(
        task: TaskCreateSchema,
        user_id: int,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
):
    task_id = await task_repository.create_task(
        task,
        user_id=user_id
    )
    return task_id
