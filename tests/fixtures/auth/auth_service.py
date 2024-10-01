import pytest

from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest.fixture
def mock_auth_service(
    yandex_client, google_client, fake_user_repository
) -> AuthService:
    return AuthService(
        user_repository=fake_user_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        settings=Settings(),
    )


@pytest.fixture
def auth_service(yandex_client, google_client, db_session) -> AuthService:
    return AuthService(
        user_repository=UserRepository(db_session=db_session),
        google_client=google_client,
        yandex_client=yandex_client,
        settings=Settings(),
    )
