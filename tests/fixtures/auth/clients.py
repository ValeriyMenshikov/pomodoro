import dataclasses

import pytest
from faker import Faker as FakerFactory
from app.settings import Settings
from app.users.auth.clients import GoogleClient
from app.users.auth.clients.base_client import BaseClient
from app.users.auth.clients.configuration import Configuration
from app.users.auth.schema import GoogleUserData

faker = FakerFactory()


@dataclasses.dataclass
class FakeGoogleClient:
    settings: Settings
    client: BaseClient

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_user_access_token(code=code)
        return google_user_info_data()

    async def _get_user_access_token(self, code: str) -> str:
        return "access_token"


@dataclasses.dataclass
class FakeYandexClient:
    settings: Settings
    client: BaseClient

    async def get_user_info(self, code: str) -> dict:
        return {"email": "g5h9E@example.com"}

    async def _get_user_access_token(self, code: str) -> str:
        return "access_token"


@pytest.fixture
def google_client() -> FakeGoogleClient:
    return FakeGoogleClient(
        settings=Settings(),
        client=BaseClient(configuration=Configuration(host='', disable_log=False)),
    )


@pytest.fixture
def yandex_client() -> FakeYandexClient:
    return FakeYandexClient(
        settings=Settings(),
        client=BaseClient(configuration=Configuration(host='', disable_log=False)),
    )


# @pytest.fixture
def google_user_info_data() -> GoogleUserData:
    return GoogleUserData(
        id=str(faker.random_int()),
        email=faker.email(),
        name=faker.name(),
        verified_email=True,
        google_access_token=faker.sha256()
    )
