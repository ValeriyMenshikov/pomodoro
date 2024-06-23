from app.handlers.task import router as task_router
from app.handlers.user import router as user_router
from app.handlers.auth import router as auth_router

routers = [
    task_router,
    user_router,
    auth_router
]
