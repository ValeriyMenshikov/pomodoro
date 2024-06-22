from fastapi import APIRouter

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
    response_model=TasksSchema
)
async def get_tasks() -> list[TaskSchema]:
    return [_ for _ in range(10)]


@router.get(
    "/{task_id}",
    response_model=TaskSchema
)
async def get_task(task_id: int) -> TaskSchema:
    return TaskSchema


@router.put(
    "/{task_id}",
    response_model=TaskCreateSchema
)
async def update_task(task: TaskCreateSchema) -> TaskCreateSchema:
    return TaskCreateSchema


@router.post(
    "/task",
    response_model=TaskCreateSchema
)
async def create_task(task: TaskCreateSchema) -> TaskCreateSchema:
    return TasksSchema
