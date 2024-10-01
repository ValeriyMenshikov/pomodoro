from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.users.user_profile.schema import (
    UserCreateSchema,
)
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.service import UserService
from app.dependency import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post("/create")
async def create_user(
    user: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> UserLoginSchema:
    result = await user_service.create_user(user.username, user.password)
    return result
