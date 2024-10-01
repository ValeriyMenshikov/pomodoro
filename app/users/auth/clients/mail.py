import asyncio
import json
import uuid
from dataclasses import dataclass
import aio_pika

from app.broker.producer import BrokerProducer
from app.settings import Settings


@dataclass
class MailClient:
    settings: Settings
    broker_producer: BrokerProducer

    async def send_welcome_email(self, to: str) -> None:
        body = {
            "message": f"Welcome to Pomodoro!",
            "user_email": to,
            "subject": "Welcome to Pomodoro!",
        }
        await self.broker_producer.send(message=body)
