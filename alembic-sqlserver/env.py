import os
import sys
from logging.config import fileConfig
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Import SQL Server-specific models
from marketdata_api.database.base import Base
from marketdata_api.models.sqlserver.instrument import SqlServerInstrument, SqlServerTradingVenue
from marketdata_api.models.sqlserver.legal_entity import SqlServerLegalEntity, SqlServerEntityAddress, SqlServerEntityRegistration, SqlServerEntityRelationship, SqlServerEntityRelationshipException
from marketdata_api.models.sqlserver.figi import SqlServerFigiMapping
from marketdata_api.models.sqlserver.transparency import SqlServerTransparencyCalculation
from marketdata_api.models.sqlserver.market_identification_code import SqlServerMarketIdentificationCode

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata

def get_sql_server_url():
    """Build SQL Server connection URL from environment variables."""
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE") 
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    port = os.getenv("AZURE_SQL_PORT", "1433")
    
    if not all([server, database, username, password]):
        raise ValueError("Missing required SQL Server environment variables")
    
    # URL encode the password to handle special characters
    password_encoded = quote_plus(password)
    
    return (
        f"mssql+pyodbc://{username}:{password_encoded}@"
        f"{server}:{port}/{database}"
        f"?driver=SQL+Server"
    )

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    try:
        url = get_sql_server_url()
    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure all Azure SQL environment variables are set:")
        print("- AZURE_SQL_SERVER")
        print("- AZURE_SQL_DATABASE") 
        print("- AZURE_SQL_USERNAME")
        print("- AZURE_SQL_PASSWORD")
        return
        
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    try:
        url = get_sql_server_url()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Override the URL in the config
    config.set_main_option("sqlalchemy.url", url)
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()