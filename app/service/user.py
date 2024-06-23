import string
from dataclasses import dataclass

from app.models import UserProfile
from app.repository import UserRepository
from app.schemas import UserLoginSchema
from random import choice


@dataclass
class UserService:
    user_repository: UserRepository

    async def create_user(self, user_name: str, password: str) -> UserLoginSchema:
        access_token = await self._generate_access_token()
        user: UserProfile = await self.user_repository.create_user(user_name, password, access_token)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    @staticmethod
    async def _generate_access_token() -> str:
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(32))
