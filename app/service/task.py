from dataclasses import dataclass

from app.exception import TaskNotFound
from app.repository.cache_tasks import TaskCache
from app.repository import TaskRepository
from app.schemas.task import (
    TasksSchema,
    TaskSchema,
    CreateOrUpdateTaskSchema,
)


@dataclass
class TaskService:
    task_cache: TaskCache
    task_repository: TaskRepository

    async def get_tasks(self) -> TasksSchema:
        tasks_list = await self.task_cache.get_tasks()
        if tasks_list.tasks:
            return tasks_list

        tasks = await self.task_repository.get_tasks()
        tasks_schema = TasksSchema(tasks=[TaskSchema.model_validate(task) for task in tasks])
        await self.task_cache.set_tasks(tasks=tasks_schema)
        result = await self.task_cache.get_tasks()
        return result

    async def create_task(self, task: CreateOrUpdateTaskSchema, user_id: int) -> TaskSchema:
        task = await self.task_repository.create_task(task=task, user_id=user_id)
        return TaskSchema.model_validate(task)

    async def update_task(self, task: CreateOrUpdateTaskSchema, task_id: int, user_id: int) -> TaskSchema:
        user_task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not user_task:
            raise TaskNotFound
        task = await self.task_repository.update_task(task=task, task_id=task_id, user_id=user_id)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: int, user_id: int) -> None:
        user_task = await self.task_repository.get_user_task(task_id=task_id, user_id=user_id)
        if not user_task:
            raise TaskNotFound
        await self.task_repository.delete_task(task_id=task_id, user_id=user_id)