from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.interfaces import ItemRepositoryProtocol
from app.domain.models import Item
from app.infrastructure.db import ItemORM


class SqlAlchemyItemRepository(ItemRepositoryProtocol):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, item_id: int) -> Optional[Item]:
        res = await self._session.get(ItemORM, item_id)
        if not res:
            return None
        return Item(
            id=res.id,
            title=res.title,
            description=res.description,
            is_active=res.is_active,
            created_at=res.created_at
        )

    async def list_all(self, limit: int = 100, offset: int = 0) -> list[Item]:
        stmt = select(ItemORM).offset(offset).limit(limit)
        res = await self._session.execute(stmt)
        return [
            Item(
                id=row.id,
                title=row.title,
                description=row.description,
                is_active=row.is_active,
                created_at=row.created_at
            )
            for row in res.scalars().all()
        ]

    async def save(self, item: Item) -> Item:
        if item.id is None:
            orm = ItemORM(
                title=item.title,
                description=item.description,
                is_active=item.is_active,
                created_at=item.created_at
            )
            self._session.add(orm)
            await self._session.commit()
            await self._session.refresh(orm)
            item.id = orm.id
            return item
        else:
            orm = await self._session.get(ItemORM, item.id)
            if orm:
                orm.title = item.title
                orm.description = item.description
                orm.is_active = item.is_active
                await self._session.commit()
            return item

    async def delete(self, item_id: int) -> bool:
        orm = await self._session.get(ItemORM, item_id)
        if not orm:
            return False
        await self._session.delete(orm)
        await self._session.commit()
        return True
