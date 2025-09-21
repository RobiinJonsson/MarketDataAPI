"""SQL Server optimized instrument service."""

import uuid
import logging
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import text, and_, or_
from ...services.interfaces.instrument_service_interface import InstrumentServiceInterface
from ...models.interfaces.instrument_interface import InstrumentInterface
from ...config import DatabaseConfig

logger = logging.getLogger(__name__)


class SqlServerInstrumentService(InstrumentServiceInterface):
    """SQL Server optimized instrument service using single table design."""
    
    def __init__(self):
        # Get database instance directly based on configuration
        db_type = DatabaseConfig.get_database_type()
        if db_type in ['sqlserver', 'azure_sql', 'mssql']:
            from ...database.sqlserver.sql_server_database import SqlServerDatabase
            self.db = SqlServerDatabase()
        else:
            raise ValueError(f"SqlServerInstrumentService requires SQL Server database, got: {db_type}")
        
        self.session_maker = self.db.get_session_maker()
        self.logger = logging.getLogger(__name__)
    
    def _get_session(self) -> Session:
        """Get a database session."""
        return self.session_maker()
    
    def create_instrument(self, data: Dict[str, Any], instrument_type: str = "equity") -> InstrumentInterface:
        """Create a new instrument in SQL Server."""
        session = self._get_session()
        try:
            # Validate the data
            self.validate_instrument_data(data)
            
            # Prepare data for SQL Server single table
            instrument_data = {
                'id': str(uuid.uuid4()),
                'instrument_type': instrument_type,
            }
            
            # Map common fields
            common_fields = [
                'isin', 'full_name', 'short_name', 'symbol', 'figi',
                'cfi_code', 'currency', 'trading_venue', 'lei_id',
                'commodity_derivative', 'issuer_req', 'first_trade_date',
                'termination_date', 'relevant_authority', 'relevant_venue',
                'from_date', 'technical_from_date'
            ]
            
            for field in common_fields:
                if field in data:
                    instrument_data[field] = data[field]
            
            # Map type-specific fields
            if instrument_type == 'equity':
                equity_fields = [
                    'shares_outstanding', 'market_cap', 'voting_rights_per_share',
                    'admission_approval_date', 'admission_request_date', 
                    'price_multiplier', 'exchange', 'sector', 'industry',
                    'asset_class', 'commodity_product', 'energy_type', 'oil_type',
                    'base_product', 'sub_product', 'additional_sub_product',
                    'metal_type', 'precious_metal', 'underlying_single_isin',
                    'basket_isin', 'underlying_index_isin', 'underlying_single_index_name'
                ]
                for field in equity_fields:
                    if field in data:
                        instrument_data[field] = data[field]
            
            elif instrument_type == 'debt':
                debt_fields = [
                    'total_issued_nominal', 'maturity_date', 'nominal_value_per_unit',
                    'fixed_interest_rate', 'debt_seniority', 'coupon_frequency',
                    'credit_rating', 'floating_rate_reference', 'floating_rate_term_unit',
                    'floating_rate_term_value', 'floating_rate_basis_points_spread'
                ]
                for field in debt_fields:
                    if field in data:
                        instrument_data[field] = data[field]
            
            elif instrument_type == 'future':
                future_fields = [
                    'expiration_date', 'final_settlement_date', 'delivery_type',
                    'settlement_method', 'contract_size', 'contract_unit',
                    'settlement_currency', 'final_price_type', 'transaction_type'
                ]
                for field in future_fields:
                    if field in data:
                        instrument_data[field] = data[field]
            
            # Store additional data as JSON
            additional_data = {k: v for k, v in data.items() 
                             if k not in instrument_data and k not in ['Id', 'instrument_type']}
            if additional_data:
                instrument_data['additional_data'] = json.dumps(additional_data)
            
            # Insert using raw SQL for better SQL Server performance
            columns = ', '.join(instrument_data.keys())
            placeholders = ', '.join([f':{key}' for key in instrument_data.keys()])
            
            insert_sql = f"""
            INSERT INTO instruments ({columns})
            VALUES ({placeholders})
            """
            
            result = session.execute(text(insert_sql), instrument_data)
            session.commit()
            
            # Return the created instrument
            return self.get_instrument_by_id(instrument_data['id'])
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error creating instrument: {e}")
            raise
        finally:
            session.close()
    
    def get_instrument_by_id(self, instrument_id: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ID."""
        session = self._get_session()
        try:
            result = session.execute(
                text("SELECT * FROM instruments WHERE id = :id"),
                {'id': instrument_id}
            ).fetchone()
            
            if result:
                return self._row_to_instrument(result)
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting instrument by ID {instrument_id}: {e}")
            return None
        finally:
            session.close()
    
    def get_instrument_by_isin(self, isin: str) -> Optional[InstrumentInterface]:
        """Get an instrument by its ISIN."""
        session = self._get_session()
        try:
            result = session.execute(
                text("SELECT * FROM instruments WHERE isin = :isin"),
                {'isin': isin}
            ).fetchone()
            
            if result:
                return self._row_to_instrument(result)
            return None
        
        except Exception as e:
            self.logger.error(f"Error getting instrument by ISIN {isin}: {e}")
            return None
        finally:
            session.close()
    
    def get_instruments(self, limit: int = 100, offset: int = 0, 
                       instrument_type: Optional[str] = None) -> List[InstrumentInterface]:
        """Get a list of instruments with pagination."""
        session = self._get_session()
        try:
            sql = "SELECT * FROM instruments"
            params = {'limit': limit, 'offset': offset}
            
            if instrument_type:
                sql += " WHERE instrument_type = :instrument_type"
                params['instrument_type'] = instrument_type
            
            sql += " ORDER BY created_at DESC OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"
            
            results = session.execute(text(sql), params).fetchall()
            
            return [self._row_to_instrument(row) for row in results]
        
        except Exception as e:
            self.logger.error(f"Error getting instruments: {e}")
            return []
        finally:
            session.close()
    
    def update_instrument(self, instrument_id: str, data: Dict[str, Any]) -> Optional[InstrumentInterface]:
        """Update an existing instrument."""
        session = self._get_session()
        try:
            # Build UPDATE query dynamically
            set_clauses = []
            params = {'id': instrument_id}
            
            for key, value in data.items():
                if key != 'id':  # Don't update the ID
                    set_clauses.append(f"{key} = :{key}")
                    params[key] = value
            
            if not set_clauses:
                return self.get_instrument_by_id(instrument_id)
            
            # Add updated_at timestamp
            set_clauses.append("updated_at = GETUTCDATE()")
            
            update_sql = f"""
            UPDATE instruments 
            SET {', '.join(set_clauses)}
            WHERE id = :id
            """
            
            result = session.execute(text(update_sql), params)
            session.commit()
            
            if result.rowcount > 0:
                return self.get_instrument_by_id(instrument_id)
            return None
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error updating instrument {instrument_id}: {e}")
            raise
        finally:
            session.close()
    
    def delete_instrument(self, instrument_id: str) -> bool:
        """Delete an instrument."""
        session = self._get_session()
        try:
            result = session.execute(
                text("DELETE FROM instruments WHERE id = :id"),
                {'id': instrument_id}
            )
            session.commit()
            return result.rowcount > 0
        
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error deleting instrument {instrument_id}: {e}")
            return False
        finally:
            session.close()
    
    def search_instruments(self, query: str, limit: int = 100) -> List[InstrumentInterface]:
        """Search instruments by name, symbol, or ISIN."""
        session = self._get_session()
        try:
            search_sql = """
            SELECT * FROM instruments 
            WHERE 
                isin LIKE :query OR 
                full_name LIKE :query OR 
                short_name LIKE :query OR 
                symbol LIKE :query
            ORDER BY 
                CASE 
                    WHEN isin = :exact_query THEN 1
                    WHEN symbol = :exact_query THEN 2
                    WHEN full_name LIKE :exact_query THEN 3
                    ELSE 4 
                END,
                created_at DESC
            OFFSET 0 ROWS FETCH NEXT :limit ROWS ONLY
            """
            
            params = {
                'query': f'%{query}%',
                'exact_query': query,
                'limit': limit
            }
            
            results = session.execute(text(search_sql), params).fetchall()
            
            return [self._row_to_instrument(row) for row in results]
        
        except Exception as e:
            self.logger.error(f"Error searching instruments: {e}")
            return []
        finally:
            session.close()
    
    def validate_instrument_data(self, data: Dict[str, Any]) -> None:
        """Validate instrument data."""
        required_fields = ['Id']  # At minimum, we need an ID from FIRDS
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")
    
    def enrich_with_figi(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with FIGI data."""
        # Import here to avoid circular imports
        from ...services.openfigi import search_openfigi
        
        try:
            if instrument.symbol and not instrument.figi:
                figi_data = search_openfigi(instrument.symbol)
                if figi_data and 'figi' in figi_data:
                    # Update the instrument with FIGI data
                    update_data = {'figi': figi_data['figi']}
                    self.update_instrument(instrument.id, update_data)
        except Exception as e:
            self.logger.warning(f"Failed to enrich instrument {instrument.id} with FIGI: {e}")
        
        return instrument
    
    def enrich_with_lei(self, instrument: InstrumentInterface) -> InstrumentInterface:
        """Enrich instrument with LEI data."""
        # Import here to avoid circular imports
        from ...services.gleif import fetch_lei_info
        
        try:
            if instrument.lei_id and not hasattr(instrument, '_lei_data_fetched'):
                lei_data = fetch_lei_info(instrument.lei_id)
                if lei_data:
                    # Mark as fetched to avoid repeated calls
                    setattr(instrument, '_lei_data_fetched', True)
        except Exception as e:
            self.logger.warning(f"Failed to enrich instrument {instrument.id} with LEI: {e}")
        
        return instrument
    
    def _row_to_instrument(self, row) -> InstrumentInterface:
        """Convert a database row to an instrument interface."""
        # Create a simple instrument object that implements the interface
        # For SQL Server, we'll create a dynamic object that implements the interface
        
        class SqlServerInstrumentProxy:
            """Dynamic proxy object for SQL Server instrument data."""
            
            def __init__(self, row_data):
                # Set all row data as attributes
                for key, value in row_data._mapping.items():
                    setattr(self, key, value)
                
                # Ensure we have the required interface properties
                if not hasattr(self, 'id'):
                    self.id = getattr(self, 'instrument_id', None)
                if not hasattr(self, 'isin'):
                    self.isin = None
                if not hasattr(self, 'full_name'):
                    self.full_name = None
                if not hasattr(self, 'symbol'):
                    self.symbol = None
                if not hasattr(self, 'currency'):
                    self.currency = None
                if not hasattr(self, 'instrument_type'):
                    self.instrument_type = 'unknown'
        
        return SqlServerInstrumentProxy(row)
