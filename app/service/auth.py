from dataclasses import dataclass

from app.exception import (
    UserNotFoundException,
    UserNotCorrectPasswordException,
)
from app.models import UserProfile
from app.repository import UserRepository
from app.schemas import UserLoginSchema


@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, user_name: str, password: str) -> UserLoginSchema:
        user: UserProfile = await self.user_repository.get_user_by_username(user_name)
        self._validate_auth_user(user=user, password=password)
        return UserLoginSchema(user_id=user.id, access_token=user.access_token)

    @staticmethod
    def _validate_auth_user(user: UserProfile, password: str):
        if not user:
            raise UserNotFoundException
        if user.password != password:
            raise UserNotCorrectPasswordException
