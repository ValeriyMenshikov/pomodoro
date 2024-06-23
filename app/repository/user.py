from sqlalchemy import (
    insert,
    select,
)

from app.infrastructure.database import BaseRepository
from app.models import UserProfile


class UserRepository(BaseRepository):

    async def create_user(self, user_name: str, password: str, access_token: str) -> UserProfile:
        query = insert(UserProfile).values(
            username=user_name,
            password=password,
            access_token=access_token
        ).returning(UserProfile)
        result = await self.execute(query)
        return result.scalar_one_or_none()

    async def get_user(self, user_id: int) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.id == user_id
        )
        result = await self.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, user_name: str) -> UserProfile | None:
        query = select(UserProfile).where(
            UserProfile.username == user_name
        )
        result = await self.execute(query)
        return result.scalar_one_or_none()
