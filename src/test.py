from faststream.redis import RedisBroker
from bootstrap.config import load_config_from_file, Config


async def main():
    broker = RedisBroker(load_config_from_file().message_queue_url)
    await broker.connect()
    publisher = broker.publisher("reports")
    await publisher.publish(
        {"chat_id": 1234, "report_type_id": "late_delivery_vouchers"}
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
