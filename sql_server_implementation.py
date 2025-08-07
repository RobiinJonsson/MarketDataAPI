"""
SQL Server Implementation of Unified Document-Based Approach

SQL Server has excellent JSON support and this design is actually BETTER 
on SQL Server than SQLite due to advanced JSON features.
"""

import uuid
from typing import Dict, Any, Optional
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Index, Text
from sqlalchemy.dialects.mssql import NVARCHAR, UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from .base_model import Base


class Instrument(Base):
    """SQL Server instrument model with JSON document storage."""
    __tablename__ = "instruments"
    
    # SQL Server optimized columns
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    isin = Column(NVARCHAR(12), unique=True, nullable=False, index=True)
    instrument_type = Column(NVARCHAR(50), nullable=False, index=True)
    
    # Essential fields
    full_name = Column(NVARCHAR(500))
    short_name = Column(NVARCHAR(200))
    currency = Column(NVARCHAR(3))
    cfi_code = Column(NVARCHAR(6))
    lei_id = Column(NVARCHAR(20), ForeignKey('legal_entities.lei', ondelete='SET NULL'))
    
    # JSON columns - SQL Server native JSON support
    firds_data = Column(Text)  # NVARCHAR(MAX) with JSON validation
    processed_attributes = Column(Text)  # NVARCHAR(MAX) with JSON validation
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    legal_entity = relationship("LegalEntity", back_populates="instruments")
    trading_venues = relationship("TradingVenue", back_populates="instrument", cascade="all, delete-orphan")
    figi_mapping = relationship("FigiMapping", back_populates="instrument", uselist=False)
    
    # SQL Server specific table options
    __table_args__ = (
        Index('idx_instruments_isin', 'isin'),
        Index('idx_instruments_type', 'instrument_type'),
        Index('idx_instruments_lei', 'lei_id'),
        # JSON index examples for SQL Server 2022+
        # Index('idx_instruments_json_price', text("(JSON_VALUE(processed_attributes, '$.price_multiplier'))")),
        {'schema': 'marketdata'}  # SQL Server schema
    )


class TradingVenue(Base):
    """SQL Server trading venue model."""
    __tablename__ = "trading_venues"
    
    # SQL Server optimized columns
    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    instrument_id = Column(UNIQUEIDENTIFIER, ForeignKey('marketdata.instruments.id', ondelete='CASCADE'), nullable=False)
    
    # Core venue fields
    venue_id = Column(NVARCHAR(100), nullable=False)
    isin = Column(NVARCHAR(12), nullable=False)  # Denormalized for performance
    
    # Trading dates
    first_trade_date = Column(DateTime)
    termination_date = Column(DateTime)
    admission_approval_date = Column(DateTime)
    request_for_admission_date = Column(DateTime)
    
    # Venue-specific data
    venue_full_name = Column(NVARCHAR(500))
    venue_short_name = Column(NVARCHAR(200))
    classification_type = Column(NVARCHAR(100))
    venue_currency = Column(NVARCHAR(3))
    
    # Administrative fields
    issuer_requested = Column(NVARCHAR(100))
    competent_authority = Column(NVARCHAR(100))
    relevant_trading_venue = Column(NVARCHAR(100))
    publication_from_date = Column(DateTime)
    
    # JSON column for additional attributes
    venue_attributes = Column(Text)  # NVARCHAR(MAX) with JSON
    
    # Record metadata
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    
    # Relationships
    instrument = relationship("Instrument", back_populates="trading_venues")
    
    # SQL Server indexes
    __table_args__ = (
        Index('idx_trading_venues_instrument_id', 'instrument_id'),
        Index('idx_trading_venues_venue_id', 'venue_id'),
        Index('idx_trading_venues_isin', 'isin'),
        Index('idx_trading_venues_isin_venue', 'isin', 'venue_id'),
        Index('idx_trading_venues_dates', 'first_trade_date', 'termination_date'),
        {'schema': 'marketdata'}
    )


# SQL SERVER SPECIFIC FEATURES AND OPTIMIZATIONS

"""
1. SQL SERVER JSON ADVANTAGES:

SQL Server has superior JSON support compared to SQLite:

- JSON_VALUE(): Extract scalar values from JSON
- JSON_QUERY(): Extract objects/arrays from JSON  
- JSON_MODIFY(): Update JSON values
- OPENJSON(): Convert JSON to relational data
- JSON path expressions with advanced filtering
- JSON indexes for fast queries (SQL Server 2022+)
- JSON validation constraints

2. QUERY EXAMPLES:

-- Query instruments with specific price multiplier
SELECT * FROM marketdata.instruments 
WHERE JSON_VALUE(processed_attributes, '$.price_multiplier') > 1.0;

-- Get all oil-related instruments
SELECT * FROM marketdata.instruments 
WHERE JSON_VALUE(processed_attributes, '$.asset_class.oil_type') IS NOT NULL;

-- Extract complex JSON data as table
SELECT 
    i.isin,
    i.full_name,
    attr.*
FROM marketdata.instruments i
CROSS APPLY OPENJSON(i.processed_attributes) 
WITH (
    price_multiplier float '$.price_multiplier',
    underlying_isin nvarchar(12) '$.underlying_isin',
    oil_type nvarchar(50) '$.asset_class.oil_type'
) AS attr
WHERE i.instrument_type = 'equity';

-- Venue analysis with JSON attributes
SELECT 
    tv.venue_id,
    COUNT(*) as instrument_count,
    AVG(CAST(JSON_VALUE(tv.venue_attributes, '$.settlement_period_days') AS int)) as avg_settlement
FROM marketdata.trading_venues tv
GROUP BY tv.venue_id;

3. PERFORMANCE OPTIMIZATIONS:

-- Add JSON indexes (SQL Server 2022+)
CREATE INDEX idx_instruments_price_multiplier 
ON marketdata.instruments (JSON_VALUE(processed_attributes, '$.price_multiplier'));

CREATE INDEX idx_instruments_oil_type
ON marketdata.instruments (JSON_VALUE(processed_attributes, '$.asset_class.oil_type'));

-- Add JSON constraints
ALTER TABLE marketdata.instruments 
ADD CONSTRAINT chk_instruments_json 
CHECK (ISJSON(processed_attributes) = 1);

ALTER TABLE marketdata.trading_venues 
ADD CONSTRAINT chk_venues_json 
CHECK (ISJSON(venue_attributes) = 1);

4. CONNECTION STRING EXAMPLE:

mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server&schema=marketdata

5. ALEMBIC MIGRATION FOR SQL SERVER:

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.mssql import NVARCHAR, UNIQUEIDENTIFIER

def upgrade():
    # Create schema
    op.execute("CREATE SCHEMA marketdata")
    
    # Create instruments table
    op.create_table('instruments',
        sa.Column('id', UNIQUEIDENTIFIER(), nullable=False),
        sa.Column('isin', NVARCHAR(12), nullable=False),
        sa.Column('instrument_type', NVARCHAR(50), nullable=False),
        sa.Column('full_name', NVARCHAR(500), nullable=True),
        sa.Column('short_name', NVARCHAR(200), nullable=True),
        sa.Column('currency', NVARCHAR(3), nullable=True),
        sa.Column('cfi_code', NVARCHAR(6), nullable=True),
        sa.Column('lei_id', NVARCHAR(20), nullable=True),
        sa.Column('firds_data', sa.Text(), nullable=True),
        sa.Column('processed_attributes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('isin'),
        schema='marketdata'
    )
    
    # Add JSON validation constraints
    op.execute('''
        ALTER TABLE marketdata.instruments 
        ADD CONSTRAINT chk_instruments_firds_json 
        CHECK (firds_data IS NULL OR ISJSON(firds_data) = 1)
    ''')
    
    op.execute('''
        ALTER TABLE marketdata.instruments 
        ADD CONSTRAINT chk_instruments_processed_json 
        CHECK (processed_attributes IS NULL OR ISJSON(processed_attributes) = 1)
    ''')

6. SERVICE LAYER DIFFERENCES:

# SQL Server specific JSON queries
def get_instruments_by_price_multiplier(min_multiplier: float):
    return session.query(Instrument).filter(
        text("JSON_VALUE(processed_attributes, '$.price_multiplier') >= :min_mult")
    ).params(min_mult=min_multiplier).all()

def get_oil_instruments():
    return session.query(Instrument).filter(
        text("JSON_VALUE(processed_attributes, '$.asset_class.oil_type') IS NOT NULL")
    ).all()

def update_instrument_attribute(instrument_id: str, path: str, value: str):
    session.execute(
        text('''
            UPDATE marketdata.instruments 
            SET processed_attributes = JSON_MODIFY(processed_attributes, :path, :value)
            WHERE id = :id
        '''),
        {'path': f'$.{path}', 'value': value, 'id': instrument_id}
    )
"""


# SQL SERVER CONFIGURATION

SQL_SERVER_CONFIG = {
    "connection_string": "mssql+pyodbc://username:password@server/MarketDataAPI?driver=ODBC+Driver+17+for+SQL+Server",
    "schema": "marketdata",
    "json_features": {
        "validation": True,
        "indexes": True,  # SQL Server 2022+
        "computed_columns": True
    },
    "performance": {
        "connection_pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600
    }
}

"""
SQL SERVER ADVANTAGES FOR THIS DESIGN:

1. Superior JSON support with path expressions and functions
2. JSON validation constraints ensure data integrity
3. JSON indexes for fast queries (SQL Server 2022+)
4. OPENJSON for converting JSON to relational views
5. Computed columns based on JSON values
6. Enterprise features like partitioning, compression
7. Better concurrent access handling
8. Advanced security features
9. Built-in backup and recovery
10. Query optimization for JSON workloads

MIGRATION FROM CURRENT DESIGN:

1. Create new tables in SQL Server with JSON columns
2. Export current polymorphic data
3. Transform to unified JSON structure
4. Import to new tables
5. Update service layer for SQL Server JSON functions
6. Update connection strings and configurations
7. Test and validate
8. Deploy and monitor

The unified design actually works BETTER on SQL Server than the current 
polymorphic approach due to JSON optimization and enterprise features.
"""
