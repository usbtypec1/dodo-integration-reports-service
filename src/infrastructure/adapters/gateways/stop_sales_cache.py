from typing import override
from uuid import UUID

import redis.asyncio as redis

from application.ports.gateways.stop_sales_cache import StopSalesCacheGateway


class StopSalesRedisCacheGateway(StopSalesCacheGateway):
    def __init__(
        self,
        redis_client: redis.Redis,
        key: str = "stop_sales",
    ) -> None:
        self.__redis_client = redis_client
        self.__key = key

    @override
    async def exists(self, stop_sale_id: UUID) -> bool:
        """
        Check if a stop sale exists in the Redis cache.

        Args:
            stop_sale_id (str): The ID of the stop sale to check.

        Returns:
            bool: True if the stop sale exists, False otherwise.
        """
        return await self.__redis_client.sismember(self.__key, stop_sale_id.hex)  # type: ignore[return-value]
