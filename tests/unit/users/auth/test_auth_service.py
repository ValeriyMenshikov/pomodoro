import pytest
import datetime as dt
from app.settings import Settings
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from jose import jwt

from app.users.user_profile.models import UserProfile


@pytest.mark.asyncio
async def test_get_google_redirect_url(auth_service: AuthService, settings: Settings):
    assert isinstance(auth_service, AuthService)
    expected = settings.google_redirect_url
    actual = await auth_service.get_google_redirect_url()
    assert expected == actual


@pytest.mark.asyncio
async def test_generate_access_token(auth_service: AuthService, settings: Settings):
    user_id = 1

    access_token = await auth_service.generate_access_token(user_id=user_id)

    decoded_access_token = jwt.decode(access_token, settings.JWT_SECRET, algorithms=[settings.JWT_ENCODING_ALGORITHM])
    decoded_user_id = decoded_access_token.get('user_id')
    decoded_token_expire = dt.datetime.fromtimestamp(decoded_access_token.get('expire'), tz=dt.timezone.utc)
    assert (decoded_token_expire - dt.datetime.now(tz=dt.UTC)) > dt.timedelta(days=6)
    assert user_id == decoded_user_id


@pytest.mark.asyncio
async def test_google_auth__success(auth_service: AuthService):
    response = await auth_service.google_auth(code="code")
    assert isinstance(response, UserLoginSchema)
