import pytest

from app.settings import Settings
from app.users.auth.service import AuthService


@pytest.fixture
def auth_service(yandex_client, google_client, user_repository) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        google_client=google_client,
        yandex_client=yandex_client,
        settings=Settings(),
    )
