from app.infrastructure.cache import get_redis_connection
from app.infrastructure.database import get_repository
from app.tasks.repository.cache_tasks import TaskCache

__all__ = ['get_repository', 'get_redis_connection']


async def task_cache_repository() -> 'TaskCache':
    return TaskCache(get_redis_connection())
