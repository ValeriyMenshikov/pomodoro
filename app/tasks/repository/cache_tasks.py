from redis import asyncio as Redis
import json
from app.tasks.schema import (
    TaskSchema,
    TasksSchema,
)


class TaskCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_tasks(self) -> TasksSchema:
        async with self.redis as redis:
            tasks_json = await redis.lrange("tasks", 0, -1)
            return TasksSchema(tasks=[TaskSchema.model_validate(json.loads(task)) for task in tasks_json])

    async def set_tasks(self, tasks: TasksSchema) -> None:
        tasks_json = [task.json() for task in tasks.tasks]
        async with self.redis as redis:
            for task_json in tasks_json:
                await redis.pipeline().lpush("tasks", task_json).expire("tasks", 20).execute()
