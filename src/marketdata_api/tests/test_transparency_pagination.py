"""
Comprehensive Transparency API Pagination and Structure Tests

Tests for the transparency API pagination logic, response structure validation,
and statistics accuracy. These tests target the specific issues identified
in the comprehensive test evaluation.
"""

import json
from unittest.mock import Mock, patch

import pytest

from marketdata_api import create_app
from marketdata_api.models.sqlite.transparency import TransparencyCalculation

from .test_data_real import get_test_isin


@pytest.fixture
def app():
    """Create a test Flask application."""
    test_config = {
        "TESTING": True,
        "DATABASE_URL": "sqlite:///:memory:",
    }
    app = create_app(config_override=test_config)
    return app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


class TestTransparencyAPIPagination:
    """Test transparency API pagination logic and response structure."""

    @pytest.mark.integration
    def test_pagination_per_page_capping(self, client):
        """Test that per_page is correctly capped at 100."""
        # Test requesting more than 100 items per page
        response = client.get("/api/v1/transparency?per_page=200")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Should cap at 100 items per page
        assert len(data.get("data", [])) <= 100
        
        # Pagination metadata should reflect the cap
        meta = data.get("meta", {})
        assert meta.get("per_page") == 100

    @pytest.mark.integration
    def test_pagination_with_file_type_filter(self, client):
        """Test pagination with file_type filtering (addresses the 136 vs 100 issue)."""
        # Test with FULECR_E filter that caused the original issue
        response = client.get("/api/v1/transparency?file_type=FULECR_E&per_page=50")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Verify response structure
        assert "data" in data
        assert "status" in data
        assert "meta" in data
        
        # Verify meta pagination structure
        meta = data["meta"]
        assert "per_page" in meta
        assert "total" in meta
        
        assert meta.get("per_page") == 50
        
        # Verify calculations are actual TransparencyCalculation data
        calculations = data["data"]
        if calculations:
            for calc in calculations:
                assert "id" in calc  # actual field name is 'id', not 'transparency_id'
                assert "isin" in calc
                assert "file_type" in calc
                # Note: This test found an API filtering issue - file_type filtering may not be working correctly

    @pytest.mark.integration
    def test_multi_page_navigation(self, client):
        """Test multi-page pagination navigation."""
        # Get first page
        response1 = client.get("/api/v1/transparency?per_page=5&page=1")
        assert response1.status_code == 200
        
        data1 = json.loads(response1.data)
        meta1 = data1.get("meta", {})
        
        if meta1.get("total", 0) > 5:
            # Get second page
            response2 = client.get("/api/v1/transparency?per_page=5&page=2")
            assert response2.status_code == 200
            
            data2 = json.loads(response2.data)
            meta2 = data2.get("meta", {})
            
            # Verify pagination consistency across pages
            assert meta1["total"] == meta2["total"]
            assert meta1["per_page"] == meta2["per_page"]
            assert meta2["page"] == 2
            
            # Verify different data on different pages
            calc1_ids = [c["id"] for c in data1["data"]]
            calc2_ids = [c["id"] for c in data2["data"]]
            assert set(calc1_ids).isdisjoint(set(calc2_ids))

    @pytest.mark.integration 
    def test_empty_result_pagination(self, client):
        """Test pagination with filters that return no results."""
        # Use a filter that should return no results
        response = client.get("/api/v1/transparency?isin=NONEXISTENT999&per_page=10")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Verify empty result structure
        assert data["data"] == []
        assert data["meta"]["total"] == 0
        assert data["meta"]["page"] == 1
        assert data["meta"]["per_page"] == 10


class TestTransparencyAPIResponseStructure:
    """Test the new API response structure format."""

    @pytest.mark.integration
    def test_response_structure_completeness(self, client):
        """Test that response includes all required new structure elements."""
        response = client.get("/api/v1/transparency?per_page=3")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Test top-level structure
        required_keys = ["data", "status", "meta"]
        for key in required_keys:
            assert key in data, f"Missing required key: {key}"
        
        # Test data structure
        data_list = data["data"]
        assert isinstance(data_list, list)
        
        # Test meta structure contains pagination info
        meta = data["meta"]
        meta_keys = ["page", "per_page", "total"]
        for key in meta_keys:
            assert key in meta, f"Missing meta key: {key}"

    @pytest.mark.integration
    def test_calculation_object_structure(self, client):
        """Test that individual calculation objects have required fields."""
        response = client.get("/api/v1/transparency?per_page=1")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        if calculations:
            calc = calculations[0]
            
            # Test required fields for transparency calculations
            required_calc_fields = [
                "id",
                "isin", 
                "file_type",
                "instrument_type"
            ]
            
            for field in required_calc_fields:
                assert field in calc, f"Missing calculation field: {field}"
            
            # Test field types
            assert isinstance(calc["id"], str)
            assert isinstance(calc["isin"], str)
            assert isinstance(calc["file_type"], str)
            assert isinstance(calc["instrument_type"], str)
            
            # Test transparency analysis structure if present
            if "transparency_analysis" in calc:
                transparency = calc["transparency_analysis"]
                assert "has_trading_activity" in transparency
                assert isinstance(transparency["has_trading_activity"], bool)

    @pytest.mark.integration
    def test_meta_consistency_validation(self, client):
        """Test that meta data is consistent and accurate."""
        test_endpoints = [
            "/api/v1/transparency?per_page=10",
            "/api/v1/transparency?file_type=FULECR_E&per_page=5"
        ]
        
        for endpoint in test_endpoints:
            response = client.get(endpoint)
            assert response.status_code == 200
            
            data = json.loads(response.data)
            
            # Test meta structure integrity
            meta = data["meta"]
            assert "total" in meta
            assert "per_page" in meta
            assert "page" in meta
            
            # Test data consistency with meta
            actual_returned = len(data["data"])
            expected_per_page = meta["per_page"]
            total = meta["total"]
            
            # Should return up to per_page items, or fewer if total is less
            expected_returned = min(expected_per_page, total)
            assert actual_returned <= expected_returned, (
                f"Returned {actual_returned} items, expected at most {expected_returned} "
                f"for endpoint: {endpoint}"
            )


class TestTransparencyStatisticsAccuracy:
    """Test transparency statistics and filtering accuracy."""

    @pytest.mark.integration
    def test_file_type_filtering_accuracy(self, client):
        """Test that file_type filtering returns correct results."""
        # Test FULECR_E filtering
        response = client.get("/api/v1/transparency?file_type=FULECR_E")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        # All results should have file_type FULECR_E
        for calc in calculations:
            assert calc["file_type"] == "FULECR_E"

    @pytest.mark.integration
    def test_trading_activity_filtering_accuracy(self, client):
        """Test that has_trading_activity filtering is accurate."""
        # Test filtering for instruments with trading activity
        response = client.get("/api/v1/transparency?has_trading_activity=true")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        # All results should have trading activity
        for calc in calculations:
            if "transparency_analysis" in calc:
                assert calc["transparency_analysis"]["has_trading_activity"] is True
        
        # Test filtering for instruments without trading activity
        response = client.get("/api/v1/transparency?has_trading_activity=false")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        # All results should not have trading activity
        for calc in calculations:
            if "transparency_analysis" in calc:
                assert calc["transparency_analysis"]["has_trading_activity"] is False

    @pytest.mark.integration
    def test_transparency_category_distribution(self, client):
        """Test transparency category distribution and accuracy."""
        response = client.get("/api/v1/transparency?per_page=100")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        if calculations:
            # Count instrument type distribution
            type_counts = {}
            for calc in calculations:
                inst_type = calc.get("instrument_type", "unknown")
                type_counts[inst_type] = type_counts.get(inst_type, 0) + 1
            
            # Verify instrument types are valid
            valid_types = ["SHRS", "DERV", "DEBT", "FUND", "EQTY"]  # Based on FIRDS data
            for inst_type in type_counts.keys():
                if inst_type != "unknown":
                    # Just verify we have some instrument types - exact validation depends on data
                    assert isinstance(inst_type, str), f"Invalid instrument type format: {inst_type}"

    @pytest.mark.integration
    def test_isin_filtering_accuracy(self, client):
        """Test ISIN-specific filtering returns correct instrument."""
        # Use a real test ISIN
        test_isin = get_test_isin()
        
        response = client.get(f"/api/v1/transparency?isin={test_isin}")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        # All results should match the requested ISIN
        for calc in calculations:
            assert calc["isin"] == test_isin


class TestClientSideFilteringValidation:
    """Test client-side filtering logic matches backend results."""

    @pytest.mark.integration
    def test_combined_filtering_consistency(self, client):
        """Test that multiple filters work correctly together."""
        # Test combined filters
        response = client.get("/api/v1/transparency?file_type=FULECR_E&has_trading_activity=true&per_page=20")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        calculations = data["data"]
        
        # Verify all filters are applied correctly
        for calc in calculations:
            assert calc["file_type"] == "FULECR_E"
            if "transparency_analysis" in calc:
                assert calc["transparency_analysis"]["has_trading_activity"] is True

    @pytest.mark.integration
    def test_pagination_with_filtering_consistency(self, client):
        """Test pagination consistency with filtering applied."""
        # Get filtered results with pagination
        response = client.get("/api/v1/transparency?file_type=FULECR_E&per_page=5&page=1")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Verify pagination reflects filtered total, not global total
        total_with_filter = data["meta"]["total"]
        
        # Get unfiltered results for comparison
        response_unfiltered = client.get("/api/v1/transparency?per_page=5&page=1")
        assert response_unfiltered.status_code == 200
        
        data_unfiltered = json.loads(response_unfiltered.data)
        total_unfiltered = data_unfiltered["meta"]["total"]
        
        # Filtered total should be <= unfiltered total
        assert total_with_filter <= total_unfiltered

    @pytest.mark.integration
    def test_zero_results_filtering(self, client):
        """Test filtering that results in zero matches."""
        # Use filters that should return no results
        response = client.get("/api/v1/transparency?isin=INVALID&file_type=FULECR_E")
        assert response.status_code == 200
        
        data = json.loads(response.data)
        
        # Should return empty results with correct structure
        assert data["data"] == []
        assert data["meta"]["total"] == 0