import dataclasses

import pytest

from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserProfileFactory


@dataclasses.dataclass
class FakeUsersRepository:
    async def get_user_by_email(self, email: str) -> None:
        return None

    async def create_user(self, user_data: UserCreateSchema) -> None:
        return UserProfileFactory()


@pytest.fixture
def fake_user_repository() -> FakeUsersRepository:
    return FakeUsersRepository()
