from app.infrastructure.broker.accessor import get_broker_connection
import aio_pika


async def make_amqp_consumer() -> None:
    connection = await get_broker_connection()
    channel = await connection.channel()
    queue = await channel.declare_queue("callback_mail_queue", durable=True)
    await queue.consume(consume_fail_email)


async def consume_fail_email(message: aio_pika.abc.AbstractIncomingMessage) -> None:
    async with message.process():
        correlation_id = message.correlation_id
        print(message.body.decode(), correlation_id)
