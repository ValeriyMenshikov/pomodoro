from dataclasses import dataclass

import structlog

from app.users.auth.clients.base_client import BaseClient
from app.users.auth.clients.configuration import Configuration
from app.settings import Settings
from app.users.auth.schema import GoogleUserData

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=False,
        )
    ]
)


@dataclass
class GoogleClient:
    settings: Settings
    client: BaseClient = BaseClient(
        configuration=Configuration(host="", disable_log=False)
    )

    async def get_user_info(self, code: str) -> GoogleUserData:
        access_token = await self._get_access_token(code=code)
        user_info = await self.client.get(
            path="https://www.googleapis.com/oauth2/v1/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return GoogleUserData(**user_info.json(), google_access_token=access_token)

    async def _get_access_token(self, code: str) -> str:
        data = {
            "code": code,
            "client_id": self.settings.GOOGLE_CLIENT_ID,
            "client_secret": self.settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": self.settings.GOOGLE_REDIRECT_URL,
            "grant_type": "authorization_code",
        }
        response = await self.client.post(
            path=self.settings.GOOGLE_TOKEN_URL, data=data
        )
        access_token = response.json().get("access_token")
        return access_token
