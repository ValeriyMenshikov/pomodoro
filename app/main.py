from fastapi import FastAPI
from app.tasks.handlers import router as tasks_router
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_profile_router
from worker.tasks import send_email_task

app = FastAPI()
for router in [
    tasks_router,
    auth_router,
    user_profile_router,
]:
    app.include_router(router)


def register_user(email):
    send_email_task.delay(email)
