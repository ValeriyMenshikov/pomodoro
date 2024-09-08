import datetime as dt
from datetime import timedelta
from dataclasses import dataclass
from jose import jwt

from app.users.auth.clients import GoogleClient, YandexClient
from app.exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
    TokenExpired,
    TokenNotCorrect,
)
from app.users.user_profile.models import UserProfile
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import (
    UserCreateSchema,
)
from app.users.auth.schema import (
    UserLoginSchema,
)
from app.settings import Settings


@dataclass
class AuthService:
    user_repository: UserRepository
    settings: Settings
    google_client: GoogleClient
    yandex_client: YandexClient

    async def login(self, user_name: str, password: str) -> UserLoginSchema:
        user: UserProfile = await self.user_repository.get_user_by_username(user_name)
        self._validate_auth_user(user=user, password=password)
        access_token = await self.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    async def google_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.google_client.get_user_info(code=code)
        user = await self.user_repository.get_user_by_email(email=user_data.email)
        if user:
            access_token = await self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            google_access_token=user_data.google_access_token,
            email=user_data.email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = await self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException

    async def generate_access_token(self, user_id: int) -> str:
        expire_date_unix = (dt.datetime.utcnow() + timedelta(days=7)).timestamp()
        token = jwt.encode(
            claims={
                'user_id': user_id,
                'expire': expire_date_unix,
            },
            key=self.settings.JWT_SECRET,
            algorithm=self.settings.JWT_ENCODING_ALGORITHM
        )
        return token

    async def get_user_id_from_access_token(self, access_token: str) -> int:
        try:
            payload = jwt.decode(
                token=access_token,
                key=self.settings.JWT_SECRET,
                algorithms=self.settings.JWT_ENCODING_ALGORITHM
            )
        except jwt.JWTError:
            raise TokenNotCorrect

        if payload['expire'] < dt.datetime.utcnow().timestamp():
            raise TokenExpired
        return payload['user_id']

    async def get_google_redirect_url(self) -> str:
        return self.settings.google_redirect_url

    async def get_yandex_redirect_url(self) -> str:
        return self.settings.yandex_redirect_url

    async def yandex_auth(self, code: str) -> UserLoginSchema:
        user_data = await self.yandex_client.get_user_info(code=code)
        user = await self.user_repository.get_user_by_email(email=user_data.default_email)
        if user:
            access_token = await self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)

        create_user_data = UserCreateSchema(
            yandex_access_token=user_data.access_token,
            email=user_data.default_email,
            name=user_data.name,
        )
        created_user = await self.user_repository.create_user(create_user_data)
        access_token = await self.generate_access_token(user_id=created_user.id)
        return UserLoginSchema(user_id=created_user.id, access_token=access_token)