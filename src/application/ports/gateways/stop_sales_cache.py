from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class StopSalesCacheGateway(Protocol):
    @abstractmethod
    async def exists(self, stop_sale_id: UUID) -> bool: ...
