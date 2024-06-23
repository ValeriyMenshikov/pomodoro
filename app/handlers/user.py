from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from app.schemas import (
    UserLoginSchema,
    UserCreateSchema,
)
from app.service.user import UserService
from app.dependency import get_user_service

router = APIRouter(
    prefix="/users",
    tags=["User"],
)


@router.post("/create")
async def create_user(
        user: UserCreateSchema,
        user_service: Annotated[UserService, Depends(get_user_service)]
) -> UserLoginSchema:
    result = await user_service.create_user(user.username, user.password)
    return result
