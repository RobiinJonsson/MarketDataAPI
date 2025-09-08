"""
Transparency Swagger Models

This module contains all Swagger model definitions for transparency calculation endpoints,
supporting the unified transparency architecture.
"""

from flask_restx import fields

def create_transparency_models(api, common_models):
    """
    Create transparency-related Swagger models.
    
    Args:
        api: Flask-RESTx API instance
        common_models: Dictionary of common model definitions
        
    Returns:
        dict: Dictionary of transparency model definitions
    """
    
    # Base transparency model (unified architecture)
    transparency_base = api.model('TransparencyBase', {
        'id': fields.String(required=True, description="Unique identifier"),
        'isin': fields.String(required=True, description="International Securities Identification Number"),
        'file_type': fields.String(required=True, description="FITRS file type", enum=[
            'FULECR_C', 'FULECR_E', 'FULECR_R',  # Equity types
            'FULNCR_C', 'FULNCR_D', 'FULNCR_E', 'FULNCR_F', 
            'FULNCR_H', 'FULNCR_I', 'FULNCR_J', 'FULNCR_O'  # Non-equity types
        ]),
        'instrument_category': fields.String(description="Instrument category (C, D, E, F, H, I, J, O, R)"),
        'is_equity': fields.Boolean(description="Whether this is equity transparency data"),
        'is_non_equity': fields.Boolean(description="Whether this is non-equity transparency data"),
        'is_debt_instrument': fields.Boolean(description="Whether this is specifically a debt instrument"),
        'is_derivatives_or_complex': fields.Boolean(description="Whether this is derivatives or complex instruments"),
        'instrument_classification': fields.String(description="Financial instrument classification"),
        'description': fields.String(description="Instrument description"),
        'tech_record_id': fields.Integer(description="Technical record identifier"),
        'from_date': fields.Date(description="From date"),
        'to_date': fields.Date(description="To date"),
        'liquidity': fields.Boolean(description="Liquidity indicator"),
        'total_transactions_executed': fields.Integer(description="Total number of transactions executed"),
        'total_volume_executed': fields.Float(description="Total volume of transactions executed"),
        'has_transaction_data': fields.Boolean(description="Whether record has transaction data"),
        'has_threshold_data': fields.Boolean(description="Whether record has threshold data"),
        'source_file': fields.String(description="Source FITRS filename"),
        'created_at': fields.DateTime(description="Creation timestamp"),
        'updated_at': fields.DateTime(description="Last update timestamp")
    })
    
    # Transparency details (type-specific)
    transparency_details = api.model('TransparencyDetails', {
        'type': fields.String(required=True, description="CFI-based instrument type", enum=[
            'equity', 'debt', 'collective_investment', 'future', 'structured', 
            'index_linked', 'warrant', 'option', 'rights', 'swap', 'other'
        ]),
        'financial_instrument_classification': fields.String(description="Financial instrument classification (equity only)"),
        'methodology': fields.String(description="Methodology used (equity only)"),
        'average_daily_turnover': fields.Float(description="Average daily turnover (equity only)"),
        'large_in_scale': fields.Float(description="Large in scale threshold (equity only)"),
        'average_daily_number_of_transactions': fields.Float(description="Average daily number of transactions (equity only)"),
        'average_transaction_value': fields.Float(description="Average transaction value (equity only)"),
        'standard_market_size': fields.Float(description="Standard market size (equity only)"),
        'description': fields.String(description="Description (non-equity only)"),
        'bond_type': fields.String(description="Bond type (debt only)"),
        'is_liquid': fields.Boolean(description="Liquidity indicator (debt only)"),
        'underlying_isin': fields.String(description="Underlying instrument ISIN (futures only)"),
        'is_stock_dividend_future': fields.Boolean(description="Stock dividend future indicator (futures only)"),
        'pre_trade_large_in_scale_threshold': fields.Float(description="Pre-trade large in scale threshold (non-equity)"),
        'post_trade_large_in_scale_threshold': fields.Float(description="Post-trade large in scale threshold (non-equity)"),
        'criterion_name': fields.String(description="Criterion name (non-equity)"),
        'criterion_value': fields.String(description="Criterion value (non-equity)")
    })
    
    # Detailed transparency model
    transparency_detailed = api.inherit('TransparencyDetailed', transparency_base, {
        'details': fields.Nested(transparency_details, description="Type-specific transparency details"),
        'raw_data': fields.Raw(description="Raw FITRS data in JSON format")
    })
    
    # Transparency list response
    transparency_list_response = api.model('TransparencyListResponse', {
        'status': fields.String(required=True, description="Response status", enum=["success"]),
        'data': fields.List(fields.Nested(transparency_detailed)),
        'meta': fields.Nested(common_models['pagination_meta'])
    })
    
    # Transparency detail response
    transparency_detail_response = api.model('TransparencyDetailResponse', {
        'status': fields.String(required=True, description="Response status", enum=["success"]),
        'data': fields.Nested(transparency_detailed)
    })
    
    # Transparency creation request
    transparency_create_request = api.model('TransparencyCreateRequest', {
        'isin': fields.String(required=True, description="International Securities Identification Number"),
        'instrument_type': fields.String(
            required=True, 
            description="CFI-based instrument type", 
            enum=['equity', 'debt', 'collective_investment', 'future', 'structured', 'index_linked', 'warrant', 'option', 'rights', 'swap']
        )
    })
    
    # Batch transparency request
    batch_transparency_request = api.model('BatchTransparencyRequest', {
        'file_type': fields.String(description="FITRS file type filter", enum=[
            'FULECR_C', 'FULECR_E', 'FULECR_R',  
            'FULNCR_C', 'FULNCR_D', 'FULNCR_E', 'FULNCR_F', 
            'FULNCR_H', 'FULNCR_I', 'FULNCR_J', 'FULNCR_O'
        ]),
        'instrument_category': fields.String(description="Instrument category filter (C, D, E, F, H, I, J, O, R)"),
        'is_equity': fields.Boolean(description="Filter by equity instruments"),
        'is_debt': fields.Boolean(description="Filter by debt instruments"),
        'isin_prefix': fields.String(description="ISIN prefix filter (e.g., 'NL' for Netherlands)"),
        'limit': fields.Integer(description="Maximum number of calculations to create", default=10),
        'cfi_type': fields.String(description="CFI type filter (D, F, E)", enum=['D', 'F', 'E'])
    })
    
    # Batch create transparency request
    batch_create_transparency_request = api.model('BatchCreateTransparencyRequest', {
        'records': fields.List(fields.Nested(transparency_create_request), required=True, description="List of transparency records to create")
    })
    
    # Transparency statistics
    transparency_statistics = api.model('TransparencyStatistics', {
        'total_records': fields.Integer(description="Total transparency records"),
        'equity_records': fields.Integer(description="Number of equity records"),
        'non_equity_records': fields.Integer(description="Number of non-equity records"),
        'by_file_type': fields.Raw(description="Count by FITRS file type"),
        'by_instrument_category': fields.Raw(description="Count by instrument category"),
        'last_update': fields.DateTime(description="Last data update timestamp"),
        'coverage_stats': fields.Nested(api.model('CoverageStats', {
            'instruments_with_transparency': fields.Integer(description="Instruments with transparency data"),
            'unique_isins': fields.Integer(description="Unique ISINs in transparency data"),
            'date_range': fields.Nested(api.model('DateRange', {
                'earliest': fields.Date(description="Earliest transparency date"),
                'latest': fields.Date(description="Latest transparency date")
            }))
        }))
    })
    
    # Transparency statistics response
    transparency_statistics_response = api.model('TransparencyStatisticsResponse', {
        'status': fields.String(required=True, description="Response status", enum=["success"]),
        'data': fields.Nested(transparency_statistics)
    })
    
    return {
        'transparency_base': transparency_base,
        'transparency_detailed': transparency_detailed,
        'transparency_details': transparency_details,
        'transparency_list_response': transparency_list_response,
        'transparency_detail_response': transparency_detail_response,
        'transparency_create_request': transparency_create_request,
        'batch_transparency_request': batch_transparency_request,
        'batch_create_transparency_request': batch_create_transparency_request,
        'transparency_statistics': transparency_statistics,
        'transparency_statistics_response': transparency_statistics_response
    }
