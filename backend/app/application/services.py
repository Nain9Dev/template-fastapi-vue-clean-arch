from app.application.schemas import ItemCreate, ItemRead
from app.domain.interfaces import ItemRepositoryProtocol
from app.domain.models import EntityNotFoundException, Item


class ItemService:
    def __init__(self, repository: ItemRepositoryProtocol):
        self._repo = repository

    async def create_item(self, payload: ItemCreate) -> ItemRead:
        item = Item.create(title=payload.title, description=payload.description or "")
        saved = await self._repo.save(item)
        return ItemRead.model_validate(saved)

    async def get_item(self, item_id: int) -> ItemRead:
        item = await self._repo.get_by_id(item_id)
        if not item:
            raise EntityNotFoundException(f"Item with ID {item_id} was not found.")
        return ItemRead.model_validate(item)

    async def list_items(self, limit: int = 100, offset: int = 0) -> list[ItemRead]:
        items = await self._repo.list_all(limit=limit, offset=offset)
        return [ItemRead.model_validate(i) for i in items]

    async def delete_item(self, item_id: int) -> bool:
        deleted = await self._repo.delete(item_id)
        if not deleted:
            raise EntityNotFoundException(f"Item with ID {item_id} was not found.")
        return True
