from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional


class DomainException(Exception):
    """Base exception for all domain invariant violations."""
    pass


class EntityNotFoundException(DomainException):
    """Raised when a requested entity does not exist."""
    pass


@dataclass
class Item:
    id: Optional[int]
    title: str
    description: str
    is_active: bool
    created_at: datetime

    @classmethod
    def create(cls, title: str, description: str) -> "Item":
        clean_title = title.strip()
        if not clean_title or len(clean_title) < 3:
            raise DomainException("Item title must contain at least 3 non-whitespace characters.")
        return cls(
            id=None,
            title=clean_title,
            description=description.strip(),
            is_active=True,
            created_at=datetime.now(timezone.utc)
        )
