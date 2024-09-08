from pydantic import BaseModel, Field


class GoogleUserData(BaseModel):
    id: str
    email: str
    verified_email: bool
    name: str
    google_access_token: str


class YandexUserData(BaseModel):
    id: str
    login: str
    name: str = Field(None, alias='real_name')
    default_email: str
    access_token: str
