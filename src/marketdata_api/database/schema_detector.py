"""
Database Schema Analysis

This module analyzes the current database schema and provides information
about available tables, columns, and migration status for monitoring and debugging.
"""

import logging
from typing import Dict, List, Optional, Set

from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from ..config import DATABASE_TYPE
from .base import engine

logger = logging.getLogger(__name__)


class SchemaAnalyzer:
    """Analyzes database schema for monitoring and debugging"""

    def __init__(self):
        self.schema_info: Dict = {}
        self.available_tables: Set[str] = set()
        self.available_columns: Dict[str, Set[str]] = {}
        self.migration_level: Optional[str] = None

    def analyze_schema(self) -> Dict:
        """Analyze current database schema"""
        try:
            self._detect_tables()
            self._detect_columns()
            self._detect_migration_level()

            logger.info(f"Schema analysis complete:")
            logger.info(f"  - Tables: {len(self.available_tables)}")
            logger.info(f"  - Migration level: {self.migration_level or 'Unknown'}")

            has_transparency = "transparency_calculations" in self.available_tables

            return {
                "tables": self.available_tables,
                "columns": self.available_columns,
                "migration_level": self.migration_level,
                "has_transparency": has_transparency,
                "has_entity_relationships": "entity_relationships" in self.available_tables,
                "has_related_isins": "related_isins" in self.available_tables,
                "has_figi_mappings": "figi_mappings" in self.available_tables,
                "table_count": len(self.available_tables),
                "is_fully_migrated": has_transparency and self.migration_level is not None,
            }

        except Exception as e:
            logger.error(f"Schema analysis failed: {e}")
            return {"error": str(e), "tables": set(), "columns": {}}

    def _detect_tables(self):
        """Detect available tables"""
        try:
            with engine.connect() as conn:
                if DATABASE_TYPE.lower() == "azure_sql":
                    result = conn.execute(
                        text(
                            """
                        SELECT TABLE_NAME 
                        FROM INFORMATION_SCHEMA.TABLES 
                        WHERE TABLE_TYPE = 'BASE TABLE'
                    """
                        )
                    )
                else:
                    # SQLite
                    result = conn.execute(
                        text(
                            """
                        SELECT name FROM sqlite_master 
                        WHERE type='table' AND name NOT LIKE 'sqlite_%'
                    """
                        )
                    )

                self.available_tables = {row[0] for row in result.fetchall()}

        except Exception as e:
            logger.warning(f"Could not detect tables: {e}")
            self.available_tables = set()

    def _detect_columns(self):
        """Detect available columns for each table"""
        try:
            for table in self.available_tables:
                self.available_columns[table] = self._get_table_columns(table)

        except Exception as e:
            logger.warning(f"Could not detect columns: {e}")

    def _get_table_columns(self, table_name: str) -> Set[str]:
        """Get columns for a specific table"""
        try:
            with engine.connect() as conn:
                if DATABASE_TYPE.lower() == "azure_sql":
                    result = conn.execute(
                        text(
                            f"""
                        SELECT COLUMN_NAME 
                        FROM INFORMATION_SCHEMA.COLUMNS 
                        WHERE TABLE_NAME = '{table_name}'
                    """
                        )
                    )
                else:
                    # SQLite
                    result = conn.execute(text(f"PRAGMA table_info({table_name})"))
                    # SQLite returns (cid, name, type, notnull, dflt_value, pk)
                    return {row[1] for row in result.fetchall()}

                return {row[0] for row in result.fetchall()}

        except Exception as e:
            logger.warning(f"Could not get columns for {table_name}: {e}")
            return set()

    def _detect_migration_level(self):
        """Detect current Alembic migration level"""
        try:
            with engine.connect() as conn:
                # Check if alembic_version table exists
                if DATABASE_TYPE.lower() == "azure_sql":
                    result = conn.execute(
                        text(
                            """
                        SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
                        WHERE TABLE_NAME = 'alembic_version'
                    """
                        )
                    )
                else:
                    result = conn.execute(
                        text(
                            """
                        SELECT COUNT(*) FROM sqlite_master 
                        WHERE type='table' AND name='alembic_version'
                    """
                        )
                    )

                if result.fetchone()[0] > 0:
                    # Get current version
                    version_result = conn.execute(text("SELECT version_num FROM alembic_version"))
                    version = version_result.fetchone()
                    if version:
                        self.migration_level = version[0]

        except Exception as e:
            logger.warning(f"Could not detect migration level: {e}")

    def get_table_info(self, table_name: str) -> Dict:
        """Get detailed information about a specific table"""
        if table_name not in self.available_tables:
            return {"error": f"Table {table_name} not found"}

        try:
            with engine.connect() as conn:
                # Get row count
                count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                row_count = count_result.fetchone()[0]

                columns = self.available_columns.get(table_name, set())

                return {
                    "name": table_name,
                    "columns": list(columns),
                    "column_count": len(columns),
                    "row_count": row_count,
                }

        except Exception as e:
            return {"error": f"Could not analyze table {table_name}: {e}"}


# Global schema analyzer instance
schema_analyzer = SchemaAnalyzer()


def get_schema_info() -> Dict:
    """Get current schema information"""
    return schema_analyzer.analyze_schema()


def get_table_info(table_name: str) -> Dict:
    """Get information about a specific table"""
    return schema_analyzer.get_table_info(table_name)
