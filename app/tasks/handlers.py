from fastapi import (
    APIRouter,
    Depends,
)

from app.dependency import (
    get_repository,
    task_cache_repository,
)
from app.tasks.repository.cache_tasks import TaskCache
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
    response_model=TasksSchema
)
async def get_tasks(
        task_repository: TaskRepository = Depends(get_repository(TaskRepository)),
        task_cache: TaskCache = Depends(task_cache_repository)
) -> TasksSchema:
    tasks_list = await task_cache.get_tasks()
    if tasks_list.tasks:
        return tasks_list

    tasks = await task_repository.get_tasks()
    tasks_schema = TasksSchema(tasks=[TaskSchema.model_validate(task) for task in tasks])
    await task_cache.set_tasks(tasks_schema)
    result = await task_cache.get_tasks()
    return result


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
    response_model=TaskSchema
)
async def update_task(
        task_id: int,
        task: TaskCreateSchema,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository)),
) -> TaskSchema:
    task = await task_repository.update_task(task=task, task_id=task_id)
    return TaskSchema.model_validate(task)


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
