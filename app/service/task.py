from dataclasses import dataclass

from app.repository.cache_tasks import TaskCache
from app.repository import TaskRepository
from app.schemas.task import (
    TasksSchema,
    TaskSchema,
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
        await self.task_cache.set_tasks(tasks_schema)
        result = await self.task_cache.get_tasks()
        return result
