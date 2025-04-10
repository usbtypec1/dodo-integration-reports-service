from faststream.redis import RedisBroker


async def main():
    async with RedisBroker() as broker:
        await broker.publisher("all-chats-report").publish(
            {"report_type_id": "stop_sales_by_sales_channels"}
        )


import asyncio

asyncio.run(main())
