from dataclasses import dataclass

from app.tasks.repository.cache_tasks import TaskCache
from app.tasks.repository.task import TaskRepository
from app.tasks.schema import (
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
