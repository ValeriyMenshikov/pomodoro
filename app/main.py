from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends

from app.dependency import get_mail_client
# from app.consumer import make_amqp_consumer
from app.tasks.handlers import router as tasks_router
from app.users.auth.clients.mail import MailClient
from app.users.auth.handlers import router as auth_router
from app.users.user_profile.handlers import router as user_profile_router


@asynccontextmanager
async def lifespan(
        app: FastAPI,
):
    # await make_amqp_consumer()
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/message")
async def send_message(
        message: str,
        mail_client: Annotated[MailClient, Depends(get_mail_client)],
):
    respone = await mail_client.send_welcome_email(message)
    print(respone)


for router in [
    tasks_router,
    auth_router,
    user_profile_router,
]:
    app.include_router(router)
