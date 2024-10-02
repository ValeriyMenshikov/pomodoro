from dataclasses import dataclass

import structlog

from app.users.auth.clients.base_client import BaseClient
from app.users.auth.clients.configuration import Configuration
from app.users.auth.schema import YandexUserData
from app.settings import Settings

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=False,
        )
    ]
)


@dataclass
class YandexClient:
    settings: Settings
    client: BaseClient = BaseClient(
        configuration=Configuration(host="", disable_log=False)
    )

    async def get_user_info(self, code: str):
        access_token = await self._get_access_token(code=code)
        user_info = await self.client.get(
            "https://login.yandex.ru/info?format=json",
            headers={"Authorization": f"OAuth {access_token}"},
        )
        return YandexUserData(**user_info.json(), access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        response = await self.client.post(
            self.settings.YANDEX_TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": self.settings.YANDEX_CLIENT_ID,
                "client_secret": self.settings.YANDEX_CLIENT_SECRET,
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
        return response.json()["access_token"]
