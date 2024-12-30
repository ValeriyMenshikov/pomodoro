import asyncio

import aiokafka


async def main():
    consumer = aiokafka.AIOKafkaConsumer("email", bootstrap_servers="localhost:9092")
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                "{}:{:d}:{:d}: key={} value={} timestamp_ms={}".format(
                    msg.topic,
                    msg.partition,
                    msg.offset,
                    msg.key,
                    msg.value,
                    msg.timestamp,
                )
            )
    finally:
        await consumer.stop()

asyncio.run(main())
