from sqlalchemy import (
    insert,
    select,
)

from app.infrastructure.database import BaseRepository
from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema


class UserRepository(BaseRepository):

    async def create_user(self, user_data: UserCreateSchema) -> UserProfile:
        # query = insert(UserProfile).values(
        #     username=user_data.username,
        #     password=user_data.google_access_token,
        # ).returning(UserProfile)
        query = insert(UserProfile).values(**user_data.model_dump(exclude_none=True)).returning(UserProfile)

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

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
