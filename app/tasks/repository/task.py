from sqlalchemy import (
    select,
    delete,
    update,
    insert,
)
from app.infrastructure.database.base_repositoty import BaseRepository
from app.tasks.models import (
    Tasks,
    Categories,
)
from app.tasks.schema import TaskCreateSchema


class TaskRepository(BaseRepository):

    async def get_tasks(self) -> list[Tasks]:
        task: list[Tasks] = (await self.execute(select(Tasks))).scalars().all()
        return task

    async def get_task(self, task_id: int) -> Tasks | None:
        task: Tasks = (await self.execute(select(Tasks).where(Tasks.id == task_id))).scalar_one_or_none()
        return task

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        task: Tasks = (await self.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = insert(Tasks).values(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
            user_id=user_id
        ).returning(Tasks.id)
        task_id = (await self.execute(query)).scalar_one_or_none()
        return task_id

    async def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        await self.execute(query)

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(
            Categories.name == category_name
        )
        task: list[Tasks] = (await self.execute(query)).scalars().all()
        return task

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        task_id: int = (await self.execute(query)).scalar_one_or_none()
        return await self.get_task(task_id)
