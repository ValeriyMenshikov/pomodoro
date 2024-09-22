from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = '0.0.0.0'
    DB_PORT: int = 5432
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'password'
    DB_DRIVER: str = 'postgresql+asyncpg'
    DB_NAME: str = 'pomodoro'
    CACHE_HOST: str = '0.0.0.0'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    JWT_SECRET: str = 'secret'
    JWT_ENCODING_ALGORITHM: str = 'HS256'
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URL: str = ""
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REDIRECT_URI: str = ""
    YANDEX_TOKEN_URL: str = "https://oauth.yandex.ru/token"
    CELERY_REDIS_URL: str = "redis://localhost:6379/1"
    MAIL_FROM: str = "no-reply@fitra.live"
    SMTP_HOST: str = "smtp.yandex.run"
    SMTP_PORT: int = 465
    SMTP_PASSWORD: str = ""

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def google_redirect_url(self):
        return f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={self.GOOGLE_CLIENT_ID}&redirect_uri={self.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"

    @property
    def yandex_redirect_url(self):
        return f"https://oauth.yandex.ru/authorize?response_type=code&client_id={self.YANDEX_CLIENT_ID}&force_confirm=yes"
