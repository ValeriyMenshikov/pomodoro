from pydantic import (
    BaseModel,
    model_validator,
    Field,
)
from enum import Enum


class CategoryEnum(int, Enum):
    work = 1
    study = 2
    other = 3


class TaskSchema(BaseModel):
    class Config:
        from_attributes = True

    id: int = Field(...)
    name: str = Field(...)
    pomodoro_count: int = Field(...)
    category_id: int = Field(...)
    user_id: int = Field(...)

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self


class TasksSchema(BaseModel):
    tasks: list[TaskSchema] = Field(None)


class CreateOrUpdateTaskSchema(BaseModel):
    name: str = Field(...)
    pomodoro_count: int = Field(...)
    category_id: int = Field(...)
    user_id: int = Field(...)
