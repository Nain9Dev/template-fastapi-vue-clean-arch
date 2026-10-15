from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.application.schemas import HealthResponse, ItemCreate, ItemRead
from app.application.services import ItemService
from app.core.config import settings
from app.domain.models import DomainException, EntityNotFoundException
from app.infrastructure.db import get_db_session
from app.infrastructure.repositories import SqlAlchemyItemRepository

router = APIRouter()


def get_item_service(session: AsyncSession = Depends(get_db_session)) -> ItemService:
    repo = SqlAlchemyItemRepository(session)
    return ItemService(repo)


@router.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Returns runtime health and database connectivity status."""
    return HealthResponse(
        status="operational",
        version="1.0.0",
        environment=settings.ENVIRONMENT,
        database="connected"
    )


@router.get("/items", response_model=list[ItemRead], tags=["Items"])
async def list_items(
    limit: int = 100,
    offset: int = 0,
    service: ItemService = Depends(get_item_service)
) -> list[ItemRead]:
    return await service.list_items(limit=limit, offset=offset)


@router.post("/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED, tags=["Items"])
async def create_item(
    payload: ItemCreate,
    service: ItemService = Depends(get_item_service)
) -> ItemRead:
    try:
        return await service.create_item(payload)
    except DomainException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"title": "Domain Validation Error", "detail": str(e)}
        )


@router.get("/items/{item_id}", response_model=ItemRead, tags=["Items"])
async def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
) -> ItemRead:
    try:
        return await service.get_item(item_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"title": "Not Found", "detail": str(e)}
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Items"])
async def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
) -> None:
    try:
        await service.delete_item(item_id)
    except EntityNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"title": "Not Found", "detail": str(e)}
        )
