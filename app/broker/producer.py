import json
from dataclasses import dataclass
from aiokafka import AIOKafkaProducer


@dataclass
class BrokerProducer:
    producer: AIOKafkaProducer
    topic: str

    async def connect(self) -> None:
        await self.producer.start()

    async def disconnect(self) -> None:
        await self.producer.stop()

    async def send(self, message: dict) -> None:
        await self.connect()
        try:
            await self.producer.send_and_wait(self.topic, json.dumps(message).encode())
        except Exception as e:
            print(e)
        finally:
            await self.disconnect()
