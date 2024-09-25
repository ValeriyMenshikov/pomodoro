import pytest

from app.settings import Settings

pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.auth.clients",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.users.user_model",
]


@pytest.fixture
def settings():
    return Settings()
