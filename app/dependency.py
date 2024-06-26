from typing import Annotated
import redis
from fastapi import (
    Depends,
    Request,
    security,
    Security,
    HTTPException,
)

from app.exception import (
    TokenExpired,
    TokenNotCorrect,
)
from app.infrastructure.cache import get_redis_connection
from app.infrastructure.database import get_repository
from app.repository.cache_tasks import TaskCache
from app.repository import (
    TaskRepository,
    UserRepository,
)
from app.service import (
    TaskService,
    UserService,
    AuthService,
)

__all__ = [
    "get_repository",
    "get_redis_connection",
    "task_cache_repository",
    "get_task_service",
    "get_user_service",
    "get_auth_service",
]

from app.settings import Settings


async def task_cache_repository(
        redis_session: Annotated[redis.Redis, Depends(get_redis_connection)]
) -> TaskCache:
    return TaskCache(redis=redis_session)


async def get_task_service(
        task_repository: Annotated[TaskRepository, Depends(get_repository(TaskRepository))],
        cache_repository: Annotated[TaskCache, Depends(task_cache_repository)],
) -> TaskService:
    return TaskService(task_repository=task_repository, task_cache=cache_repository)


async def get_auth_service(
        user_repository: Annotated[UserRepository, Depends(get_repository(UserRepository))],
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings()
    )


async def get_user_service(
        user_repository: Annotated[UserRepository, Depends(get_repository(UserRepository))],
        auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service
    )


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        token: Annotated[security.http.HTTPAuthorizationCredentials, Security(reusable_oauth2)],
) -> int:
    try:
        user_id = await auth_service.get_user_id_from_access_token(token.credentials)
    except (TokenExpired, TokenNotCorrect) as e:
        raise HTTPException(status_code=401, detail=e.details)
    return user_id
