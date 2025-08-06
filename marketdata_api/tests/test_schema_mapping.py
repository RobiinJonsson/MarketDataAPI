import pytest
from datetime import datetime
from ..schema.schema_mapper import SchemaMapper
from ..models.sqlite.instrument import Equity, Debt
from ..database.model_mapper import map_to_model

@pytest.fixture
def schema_mapper():
    return SchemaMapper()

@pytest.fixture
def sample_equity():
    return Equity(
        isin="SE0000108656",
        full_name="Test Equity",
        short_name="TEST",
        symbol="TEST",
        currency="USD",
        market_cap=1000000.00,
        sector="Technology",
        price_multiplier=1.0,
        trading_venue="XSTO"  # Add trading venue
    )

@pytest.fixture
def sample_debt():
    return Debt(
        isin="XS2332219612",
        full_name="Test Bond",
        short_name="TBOND",
        currency="EUR",
        maturity_date=datetime(2025, 1, 1).date(),
        fixed_interest_rate=0.05,
        total_issued_nominal=1000000.00
    )

@pytest.fixture
def sample_firds_data():
    return {
        'Id': 'SE0000108656',
        'FullNm': 'Test Equity',
        'ShrtNm': 'TEST',
        'NtnlCcy': 'USD',
        'ClssfctnTp': 'ESVUFR',
        'CmmdtyDerivInd': 'false',
        'PricMltplr': '1.0'
    }

class TestSchemaMapping:
    def test_schema_loading(self, schema_mapper):
        """Test that basic schemas are loaded"""
        assert "base" in schema_mapper.mappings
        assert "equity" in schema_mapper.mappings
        assert "debt" in schema_mapper.mappings

    def test_equity_mapping(self, schema_mapper, sample_equity):
        """Test basic equity mapping"""
        result = schema_mapper.map_to_schema(sample_equity, "equity")
        assert result["identifier"] == sample_equity.isin
        assert result["full_name"] == sample_equity.full_name
        assert isinstance(result["market_cap"], float)

    def test_debt_mapping(self, schema_mapper, sample_debt):
        """Test basic debt mapping"""
        result = schema_mapper.map_to_schema(sample_debt, "debt")
        assert result["identifier"] == sample_debt.isin
        assert result["fixed_interest_rate"] == sample_debt.fixed_interest_rate
        assert "maturity_date" in result

    def test_field_transformations(self, schema_mapper, sample_equity):
        """Test field value transformations"""
        result = schema_mapper.map_to_schema(sample_equity, "equity")
        assert len(str(result["market_cap"]).split(".")[-1]) <= 2

    def test_inheritance(self, schema_mapper, sample_equity):
        """Test schema inheritance"""
        result = schema_mapper.map_to_schema(sample_equity, "equity")
        # Base fields
        assert "currency" in result
        assert "trading_venue" in result
        # Equity fields
        assert "market_cap" in result
        assert "sector" in result

    def test_xml_output(self, schema_mapper, sample_equity):
        """Test XML output format"""
        result = schema_mapper.map_to_schema(sample_equity, "equity")
        xml = schema_mapper.output_as_xml({"results": [result]})
        assert '<?xml version="1.0"' in xml
        assert '<instrument>' in xml
        assert f'<identifier>{sample_equity.isin}</identifier>' in xml

class TestModelIntegration:
    def test_model_mapper_integration(self, schema_mapper, sample_firds_data):
        """Test integration between model_mapper and schema_mapper"""
        # Map FIRDS data to model
        model_data = map_to_model(sample_firds_data, "equity")
        assert model_data["isin"] == sample_firds_data["Id"]
        
        # Map model to schema
        schema_data = schema_mapper.map_to_schema(model_data, "equity")
        assert schema_data["identifier"] == sample_firds_data["Id"]
        assert schema_data["currency"] == sample_firds_data["NtnlCcy"]

    def test_fallback_mapping(self, schema_mapper, sample_firds_data):
        """Test fallback to legacy mapping"""
        sample_firds_data["InvalidField"] = "Should be ignored"
        model_data = map_to_model(sample_firds_data, "equity")
        assert model_data["isin"] == sample_firds_data["Id"]
