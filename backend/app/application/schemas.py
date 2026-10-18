from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ItemBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=120, description="The name of the item")
    description: str | None = Field(default="", max_length=1000)


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    database: str
