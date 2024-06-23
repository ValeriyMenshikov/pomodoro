from sqlalchemy import (
    select,
    delete,
    update,
    insert,
)
from app.infrastructure.database.base_repositoty import BaseRepository
from app.tasks.models import (
    Task,
    Categories,
)
from app.tasks.schema import (
    CreateOrUpdateTaskSchema,
)


class TaskRepository(BaseRepository):

    async def get_tasks(self) -> list[Task]:
        task: list[Task] = (await self.execute(select(Task))).scalars().all()
        return task

    async def get_task(self, task_id: int) -> Task | None:
        query = select(Task).where(
            Task.id == task_id
        )
        task: Task = (await self.execute(query)).scalar_one_or_none()
        return task

    async def get_user_task(self, task_id: int, user_id: int) -> Task | None:
        query = select(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        task: Task = (await self.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: CreateOrUpdateTaskSchema) -> Task:
        query = insert(Task).values(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=task.user_id
        ).returning(Task)
        result = (await self.execute(query)).scalar_one_or_none()
        return result

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Task).where(
            Task.id == task_id,
            Task.user_id == user_id
        )
        await self.execute(query)

    async def get_task_by_category_name(self, category_name: str) -> list[Task]:
        query = select(Task).join(
            Categories,
            Task.category_id == Categories.id
        ).where(
            Categories.name == category_name
        )
        task: list[Task] = (await self.execute(query)).scalars().all()
        return task

    async def update_task(self, task: CreateOrUpdateTaskSchema, task_id: int) -> Task:
        query = update(Task).where(Task.id == task_id).values(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id
        ).returning(Task)
        result = (await self.execute(query)).scalar_one_or_none()
        return result
