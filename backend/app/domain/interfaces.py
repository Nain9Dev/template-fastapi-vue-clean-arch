from typing import Optional, Protocol
from app.domain.models import Item


class ItemRepositoryProtocol(Protocol):
    async def get_by_id(self, item_id: int) -> Optional[Item]:
        ...

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Item]:
        ...

    async def save(self, item: Item) -> Item:
        ...

    async def delete(self, item_id: int) -> bool:
        ...
