from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,

)
from fastapi.responses import RedirectResponse

from app.dependency import get_auth_service
from app.exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
)
from app.users.user_profile.schema import (
    UserCreateSchema
)
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService

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


@router.get("/login/google")
async def login_google(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url = await auth_service.get_google_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/google")
async def auth_google(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
) -> RedirectResponse:
    return await auth_service.google_auth(code)


@router.get("/login/yandex", response_class=RedirectResponse)
async def login_yandex(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RedirectResponse:
    redirect_url = await auth_service.get_yandex_redirect_url()
    print(redirect_url)
    return RedirectResponse(redirect_url)


@router.get("/yandex")
async def auth_yandex(
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        code: str
) -> RedirectResponse:
    return await auth_service.yandex_auth(code)