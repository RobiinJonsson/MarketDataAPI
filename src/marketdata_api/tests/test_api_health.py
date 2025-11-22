"""
API Health Check Tests

Comprehensive tests to verify all API routes and services are healthy and responding correctly.
These tests ensure that all endpoints are accessible, return proper status codes, and handle
basic operations without errors.
"""

import os
import tempfile
from unittest.mock import Mock, patch

import pytest
import requests
from flask import Flask

from marketdata_api import create_app
from marketdata_api.database.session import get_session

from .test_data_real import get_test_instrument, get_test_lei, get_test_mic


@pytest.fixture
def app():
    """Create a test Flask application."""
    # Create app with test configuration to prevent production database access
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


class TestAPIHealthChecks:
    """Test all API endpoints for basic health and accessibility."""

    @pytest.mark.integration
    def test_root_endpoint(self, client):
        """Test root endpoint is accessible."""
        response = client.get("/")
        assert response.status_code in [200, 302]  # Allow redirect to frontend

    @pytest.mark.integration
    def test_api_root_health(self, client):
        """Test API root endpoint is accessible."""
        response = client.get("/")  # Root is at /, not /api/v1/
        assert response.status_code == 200, f"API root endpoint failed with {response.status_code}"

    @pytest.mark.integration
    def test_swagger_ui_accessible(self, client):
        """Test Swagger UI is accessible."""
        response = client.get("/api/v1/swagger/")
        assert response.status_code == 200
        assert b"swagger" in response.data.lower() or b"openapi" in response.data.lower()

    @pytest.mark.integration
    def test_instrument_endpoints_health(self, client):
        """Test instrument-related endpoints are accessible."""
        endpoints = ["/api/v1/instruments/", "/api/v1/instruments/search"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            # These might return empty results but should not error
            assert response.status_code in [
                200,
                404,
            ], f"Instrument endpoint {endpoint} failed with {response.status_code}"

    @pytest.mark.integration
    def test_legal_entity_endpoints_health(self, client):
        """Test legal entity endpoints are accessible."""
        endpoints = ["/api/v1/legal-entities/", "/api/v1/legal-entities/search"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [
                200,
                404,
            ], f"Legal entity endpoint {endpoint} failed with {response.status_code}"

    @pytest.mark.integration
    def test_mic_endpoints_health(self, client):
        """Test MIC (Market Identification Code) endpoints are accessible."""
        endpoints = ["/mic/", "/mic/search"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [
                200,
                404,
            ], f"MIC endpoint {endpoint} failed with {response.status_code}"

    @pytest.mark.integration
    def test_transparency_endpoints_health(self, client):
        """Test transparency calculation endpoints are accessible."""
        endpoints = ["/api/v1/transparency/", "/api/v1/transparency/search"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [
                200,
                404,
            ], f"Transparency endpoint {endpoint} failed with {response.status_code}"

    @pytest.mark.integration
    def test_file_management_endpoints_health(self, client):
        """Test file management endpoints are accessible."""
        endpoints = ["/files/", "/files/status"]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [
                200,
                404,
            ], f"File management endpoint {endpoint} failed with {response.status_code}"

    @pytest.mark.integration
    def test_docs_endpoint_health(self, client):
        """Test documentation endpoint is accessible."""
        response = client.get("/api/v1/docs/")
        assert response.status_code == 200, f"Docs endpoint failed with {response.status_code}"


class TestServiceHealthChecks:
    """Test all core services for basic functionality."""

    @pytest.mark.integration
    def test_database_connection_service(self, test_session):
        """Test that database connection service works."""
        try:
            from sqlalchemy import text

            # Simple query to test connection using test session
            result = test_session.execute(text("SELECT 1")).fetchone()
            assert result is not None
        except Exception as e:
            pytest.fail(f"Database connection failed: {e}")

    @pytest.mark.integration
    @patch("marketdata_api.database.session.get_session")
    def test_instrument_service_health(self, mock_get_session):
        """Test instrument service basic operations."""
        from marketdata_api.services.core.instrument_service import InstrumentService

        # Mock session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        service = InstrumentService()

        # Test service can be instantiated and has expected methods
        assert hasattr(service, "get_instrument")
        assert hasattr(service, "get_instruments")  # Correct method name
        assert hasattr(service, "search_instruments")

    @pytest.mark.integration
    @patch("marketdata_api.database.session.get_session")
    def test_legal_entity_service_health(self, mock_get_session):
        """Test legal entity service basic operations."""
        from marketdata_api.services.core.legal_entity_service import LegalEntityService

        # Mock session
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        service = LegalEntityService()

        # Test service can be instantiated and has expected methods
        assert hasattr(service, "get_entity")
        assert hasattr(service, "get_all_entities")

    @pytest.mark.integration
    def test_file_management_service_health(self):
        """Test file management service basic operations."""
        from marketdata_api.services.utils.file_management_service import FileManagementService

        service = FileManagementService()

        # Test service can be instantiated and has expected methods
        assert hasattr(service, "download_and_parse_files")
        assert hasattr(service, "get_all_files")
        assert hasattr(service, "get_files_by_type")

    @pytest.mark.unit
    def test_esma_data_loader_service_health(self):
        """Test ESMA data loader service basic operations."""
        from marketdata_api.services.utils.esma_data_loader import EsmaDataLoader

        loader = EsmaDataLoader()

        # Test loader can be instantiated and has expected methods
        assert hasattr(loader, "load_mifid_file_list")
        assert hasattr(loader, "load_latest_files")
        assert hasattr(loader, "load_fca_firds_file_list")

    @pytest.mark.unit
    def test_mic_data_loader_service_health(self):
        """Test MIC data loader service basic operations."""
        # Mock session required for MICDataLoader
        from unittest.mock import Mock

        from marketdata_api.services.utils.mic_data_loader import MICDataLoader

        mock_session = Mock()
        loader = MICDataLoader(mock_session)

        # Test loader can be instantiated and has expected methods
        assert hasattr(loader, "load_from_csv")
        assert hasattr(loader, "load_from_remote_url")

    @pytest.mark.unit
    def test_gleif_service_health(self):
        """Test GLEIF service basic operations."""
        from marketdata_api.services.utils.gleif import GLEIFService

        service = GLEIFService()

        # Test service can be instantiated and has expected methods
        assert hasattr(service, "get_lei_data")
        assert hasattr(service, "get_parent_data")
        assert hasattr(service, "get_children_data")
        assert hasattr(service, "sync_relationships")

    @pytest.mark.unit
    def test_openfigi_service_health(self):
        """Test OpenFIGI service basic operations."""
        try:
            from marketdata_api.services.utils.openfigi import OpenFIGIService

            service = OpenFIGIService()

            # Test service can be instantiated and has expected methods
            assert hasattr(service, "search_figi")
        except ImportError:
            # Service might not be fully implemented yet
            pytest.skip("OpenFIGI service not available")


class TestServiceIntegration:
    """Test service integration with real data."""

    @pytest.mark.integration
    @patch("marketdata_api.database.session.get_session")
    def test_instrument_service_with_real_data(self, mock_get_session):
        """Test instrument service with real test data."""
        from marketdata_api.services.core.instrument_service import InstrumentService

        # Mock session and query results
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Use real test data
        real_instrument = get_test_instrument()

        mock_instrument = Mock()
        mock_instrument.isin = real_instrument["isin"]
        mock_instrument.full_name = real_instrument["full_name"]
        mock_instrument.instrument_type = real_instrument["instrument_type"]
        mock_instrument.currency = real_instrument["currency"]

        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_instrument

        service = InstrumentService()
        result_session, result_instrument = service.get_instrument(real_instrument["isin"])

        assert result_instrument is not None
        assert result_instrument.isin == real_instrument["isin"]

    @pytest.mark.integration
    def test_api_endpoint_with_real_data(self, client):
        """Test API endpoint returns proper JSON structure."""
        response = client.get("/api/v1/instruments/")

        # Should return JSON even if empty
        if response.status_code == 200:
            assert response.is_json
            data = response.get_json()
            assert isinstance(data, (list, dict))


class TestErrorHandling:
    """Test error handling across services and routes."""

    @pytest.mark.integration
    def test_api_handles_invalid_endpoints(self, client):
        """Test API handles invalid endpoints gracefully."""
        response = client.get("/api/v1/nonexistent-endpoint")
        assert response.status_code == 404

    @pytest.mark.integration
    def test_api_handles_invalid_methods(self, client):
        """Test API handles invalid HTTP methods gracefully."""
        response = client.delete("/api/v1/instruments/")  # DELETE might not be allowed
        assert response.status_code in [405, 501]  # Method Not Allowed or Not Implemented

    @pytest.mark.integration
    def test_api_handles_malformed_requests(self, client):
        """Test API handles malformed requests gracefully."""
        # Send malformed JSON
        response = client.post(
            "/api/v1/instruments/", data="invalid json}", content_type="application/json"
        )
        # Should return 400 Bad Request for malformed JSON
        assert (
            response.status_code == 400
        ), f"Expected 400 for malformed JSON, got {response.status_code}"

        # Verify error message structure
        data = response.get_json()
        assert data["status"] == "error"
        assert "Invalid JSON format" in data["error"]["message"]


class TestPerformanceBasics:
    """Basic performance tests to ensure services respond within reasonable time."""

    @pytest.mark.slow
    def test_api_response_times(self, client):
        """Test that API endpoints respond within reasonable time."""
        import time

        endpoints = ["/", "/api/v1/schemas/instruments", "/api/v1/instruments/", "/mic/"]

        for endpoint in endpoints:
            start_time = time.time()
            response = client.get(endpoint)
            end_time = time.time()

            response_time = end_time - start_time

            # API should respond within 5 seconds (generous for testing)
            assert response_time < 5.0, f"Endpoint {endpoint} took {response_time:.2f}s to respond"

    @pytest.mark.slow
    def test_database_query_performance(self, test_session):
        """Test basic database query performance."""
        import time
        from sqlalchemy import text

        start_time = time.time()
        try:
            # Use test session instead of production session
            test_session.execute(text("SELECT 1")).fetchone()
        except Exception:
            pytest.skip("Database connection not available")
        end_time = time.time()

        query_time = end_time - start_time

        # Database queries should be fast
        assert query_time < 2.0, f"Database query took {query_time:.2f}s"
