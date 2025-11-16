"""SQL Server base model with automatic timestamps."""

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, event
from sqlalchemy.orm import declarative_base

# Create separate MetaData for SQL Server to avoid table collisions with SQLite
SqlServerBase = declarative_base()


class SqlServerBaseModel(SqlServerBase):
    """Base model for SQL Server with automatic timestamps"""

    __abstract__ = True

    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, nullable=False, default=lambda: datetime.now(UTC))


@event.listens_for(SqlServerBaseModel, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    """Automatically update timestamp before any update"""
    target.updated_at = datetime.now(UTC)