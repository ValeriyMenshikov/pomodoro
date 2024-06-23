from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
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
    CreateOrUpdateTaskSchema,
)

router = APIRouter(
    prefix="/tasks",
    tags=["task"],
)


@router.get("", status_code=status.HTTP_200_OK)
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


@router.get("/{task_id}", status_code=status.HTTP_200_OK)
async def get_task(
        task_id: int,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
) -> TaskSchema:
    result = await task_repository.get_task(task_id=task_id)
    if result:
        return TaskSchema.model_validate(result)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
        task_id: int,
        task: CreateOrUpdateTaskSchema,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository)),
) -> TaskSchema:
    result = await task_repository.update_task(task=task, task_id=task_id)
    if result:
        return TaskSchema.model_validate(result)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post("/task", status_code=status.HTTP_201_CREATED)
async def create_task(
        task: CreateOrUpdateTaskSchema,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
) -> TaskSchema:
    result = await task_repository.create_task(
        task=task,
    )
    return TaskSchema.model_validate(result)


@router.delete("/task", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        user_id: int,
        task_repository: TaskRepository = Depends(get_repository(TaskRepository))
) -> None:
    await task_repository.delete_task(
        task_id=task_id,
        user_id=user_id,
    )
