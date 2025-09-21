from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, event

from ...database.base import Base


class BaseModel(Base):
    """Base model with automatic timestamps"""

    __abstract__ = True

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC))


@event.listens_for(BaseModel, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    """Automatically update timestamp before any update"""
    target.updated_at = datetime.now(UTC)
