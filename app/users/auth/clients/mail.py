import asyncio
import json
import uuid
from dataclasses import dataclass
import aio_pika

from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings

    async def send_welcome_email(self, to: str) -> None:
        connection = await aio_pika.connect_robust(
            self.settings.RABBIT_URL
        )
        body = {
            "message": f"Welcome to Pomodoro!",
            "user_email": to,
            "subject": "Welcome to Pomodoro!",
        }
        async with connection:
            channel = await connection.channel()

            queue = await channel.declare_queue('email_queue', durable=True)

            message = aio_pika.Message(
                body=json.dumps(body).encode(),
                correlation_id=str(uuid.uuid4()),
                reply_to="callback_mail_queue",
            )
            await channel.default_exchange.publish(
                message=message,
                routing_key=queue.name,
            )



