"""Factory for creating service instances based on database configuration."""

from typing import TYPE_CHECKING

from ...config import DatabaseConfig

if TYPE_CHECKING:
    from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface
    from ...services.interfaces.legal_entity_service_interface import LegalEntityServiceInterface
    from ...services.interfaces.transparency_service_interface import TransparencyServiceInterface


class ServicesFactory:
    """Factory for creating service instances based on database configuration."""

    @staticmethod
    def get_instrument_service() -> "InstrumentServiceInterface":
        """Get instrument service based on database type."""
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from ...services.sqlite.instrument_service import SqliteInstrumentService

            return SqliteInstrumentService()
        elif db_type == "sqlserver":
            from ...services.sqlserver.instrument_service import SqlServerInstrumentService

            return SqlServerInstrumentService()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    @staticmethod
    def get_legal_entity_service() -> "LegalEntityServiceInterface":
        """Get legal entity service based on database type."""
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from ...services.sqlite.legal_entity_service import LegalEntityService

            return LegalEntityService()
        elif db_type == "sqlserver":
            # TODO: Implement SQL Server legal entity service
            raise NotImplementedError("SQL Server legal entity service not yet implemented")
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    @staticmethod
    def get_transparency_service() -> "TransparencyServiceInterface":
        """Get transparency service based on database type."""
        db_type = DatabaseConfig.get_database_type()

        if db_type == "sqlite":
            from ...services.sqlite.transparency_service import TransparencyService

            return TransparencyService()
        elif db_type == "sqlserver":
            # TODO: Implement SQL Server transparency service
            raise NotImplementedError("SQL Server transparency service not yet implemented")
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
