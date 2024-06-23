from app.infrastructure.cache import get_redis_connection
from app.infrastructure.database import get_repository
from app.service.task import TaskService
from app.tasks.repository.cache_tasks import TaskCache
from fastapi import Depends

__all__ = ['get_repository', 'get_redis_connection', 'task_cache_repository']

from app.tasks.repository.task import TaskRepository


async def task_cache_repository() -> 'TaskCache':
    return TaskCache(get_redis_connection())


async def get_task_service(
        task_repository: TaskRepository = Depends(get_repository(TaskRepository)),
        cache_repository: TaskCache = Depends(task_cache_repository)
) -> 'TaskService':
    return TaskService(
        task_repository=task_repository,
        task_cache=cache_repository
    )
