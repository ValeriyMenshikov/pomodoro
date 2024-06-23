from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
HTTPException,
)

from app.dependency import get_auth_service
from app.exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
)
from app.schemas import UserCreateSchema, UserLoginSchema
from app.service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/login")
async def login(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        user: UserCreateSchema
) -> UserLoginSchema:
    try:
        user_data = await auth_service.login(user.username, user.password)
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.details)
    except UserNotCorrectPasswordException as e:
        raise HTTPException(status_code=401, detail=e.details)
    return user_data
