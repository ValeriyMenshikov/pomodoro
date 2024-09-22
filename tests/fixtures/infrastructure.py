# import pytest
#
# from app.infrastructure.database.access import engine, get_connection, get_repository
# from app.settings import Settings
#
# s = Settings()
#
# engine.url = f'{s.DB_DRIVER}://{s.DB_USER}:{s.DB_PASSWORD}@{s.DB_HOST}:{s.DB_PORT}/pomodoro'
#
#
# @pytest.fixture
# def settings() -> Settings:
#     return Settings()
#
#
# @pytest.fixture
# async def db_session(settings: Settings) -> None:
#     pass
