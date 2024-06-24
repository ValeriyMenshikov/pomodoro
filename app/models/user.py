from typing import Optional

from app.infrastructure.database import Base
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
)


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
