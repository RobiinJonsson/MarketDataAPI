"""Database interface defining the contract for all database implementations."""

from abc import ABC, abstractmethod

from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker


class DatabaseInterface(ABC):
    """Abstract interface for database implementations."""

    @abstractmethod
    def get_engine(self) -> Engine:
        """Get the database engine."""
        pass

    @abstractmethod
    def get_session_maker(self) -> sessionmaker:
        """Get the session maker for this database."""
        pass

    @abstractmethod
    def get_base_model(self):
        """Get the declarative base for this database."""
        pass

    @abstractmethod
    def init_db(self) -> None:
        """Initialize the database (create tables, etc.)."""
        pass
