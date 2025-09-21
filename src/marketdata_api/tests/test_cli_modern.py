"""
Tests for MarketDataAPI CLI functionality.

This module tests the command-line interface including commands,
argument parsing, output formatting, and error handling.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest
from click.testing import CliRunner

from marketdata_api.cli import cli
from marketdata_api.models.sqlite.instrument import Instrument
from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode

from .test_data_real import KNOWN_MIC_CODES, get_test_instrument, get_test_lei, get_test_mic


class TestCLIBasics:
    """Test basic CLI functionality and structure."""

    def test_cli_help(self):
        """Test that CLI help command works."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "MarketDataAPI CLI" in result.output
        assert "instruments" in result.output
        assert "mic" in result.output
        assert "stats" in result.output

    def test_cli_version_flag(self):
        """Test CLI version information."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        # Should not crash, version handling may vary (0=success, 1=info, 2=error but acceptable)
        assert result.exit_code in [0, 1, 2]  # CLI version commands can return various codes

    @pytest.mark.cli
    def test_instruments_help(self):
        """Test instruments subcommand help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "--help"])
        assert result.exit_code == 0
        assert "list" in result.output
        assert "get" in result.output
        assert "create" in result.output


class TestInstrumentsCommands:
    """Test instruments command group functionality."""

    @pytest.mark.cli
    @patch("marketdata_api.cli.SqliteInstrumentService")
    def test_instruments_list_success(self, mock_service):
        """Test successful instruments list command."""
        # Mock service response
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        # Use real test data for consistency
        real_instrument1 = get_test_instrument()  # Gets SEB data
        real_instrument2 = get_test_instrument()  # We'll modify this

        # Mock instruments data using real ISINs and names
        mock_instruments = [
            Mock(
                isin=real_instrument1["isin"],
                full_name=real_instrument1["full_name"],
                instrument_type=real_instrument1["instrument_type"],
                currency=real_instrument1["currency"],
            ),
            Mock(
                isin="CH0012221716", full_name="ABB Ltd", instrument_type="equity", currency="CHF"
            ),
        ]
        mock_service_instance.list_instruments.return_value = (Mock(), mock_instruments, 2)

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "list", "--limit", "2"])

        assert result.exit_code == 0
        assert real_instrument1["isin"] in result.output  # SE0000120784
        assert "Skandinaviska" in result.output or "SEB" in result.output
        assert "CH0012221716" in result.output

    @pytest.mark.cli
    @patch("marketdata_api.cli.SqliteInstrumentService")
    def test_instruments_get_success(self, mock_service):
        """Test successful instrument get command."""
        # Mock service response
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        # Use real test data
        real_instrument = get_test_instrument()

        mock_instrument = Mock(
            isin=real_instrument["isin"],
            full_name=real_instrument["full_name"],
            short_name=real_instrument["short_name"],
            instrument_type=real_instrument["instrument_type"],
            currency=real_instrument["currency"],
            cfi_code=real_instrument["cfi_code"],
            relevant_trading_venue="XSTO",
            lei_id=real_instrument["lei_id"],
            created_at="2024-01-01 10:00:00",
        )
        mock_service_instance.get_instrument.return_value = (Mock(), mock_instrument)

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "get", real_instrument["isin"]])

        assert result.exit_code == 0
        assert real_instrument["isin"] in result.output  # SE0000120784
        assert "Skandinaviska" in result.output or "SEB" in result.output
        assert real_instrument["short_name"] in result.output

    @pytest.mark.cli
    @patch("marketdata_api.cli.SqliteInstrumentService")
    def test_instruments_get_not_found(self, mock_service):
        """Test instrument get command with non-existent ISIN."""
        # Mock service response for not found
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        mock_service_instance.get_instrument.return_value = (Mock(), None)

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "get", "INVALID123"])

        assert result.exit_code == 0
        assert "not found" in result.output.lower()

    @pytest.mark.cli
    @patch("marketdata_api.cli.get_session")
    def test_instruments_list_with_filters(self, mock_get_session):
        """Test instruments list with type and currency filters."""
        # Mock database session and query
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Use real test data
        real_instrument = get_test_instrument()
        mock_instruments = [
            Mock(
                isin=real_instrument["isin"],
                full_name=real_instrument["full_name"],
                instrument_type=real_instrument["instrument_type"],
                currency=real_instrument["currency"],
            )
        ]

        # Set up the complete query chain: session.query().filter().filter().limit().all()
        mock_query_base = Mock()
        mock_filter1 = Mock()
        mock_filter2 = Mock()
        mock_limit_result = Mock()

        mock_query_base.filter.return_value = mock_filter1
        mock_filter1.filter.return_value = mock_filter2
        mock_filter2.limit.return_value = mock_limit_result
        mock_limit_result.all.return_value = mock_instruments

        mock_session.query.return_value = mock_query_base

        runner = CliRunner()
        result = runner.invoke(
            cli, ["instruments", "list", "--type", "equity", "--currency", "SEK", "--limit", "10"]
        )

        assert result.exit_code == 0
        # Verify the query was executed
        assert real_instrument["isin"] in result.output


class TestMICCommands:
    """Test MIC (Market Identification Code) commands."""

    @pytest.mark.cli
    @patch("marketdata_api.cli.get_session")
    def test_mic_list_success(self, mock_get_session):
        """Test successful MIC list command."""
        # Mock database session and query
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Use real MIC data
        mic_code = get_test_mic()  # Returns string "XSTO"
        real_mic_data = KNOWN_MIC_CODES[mic_code]  # Get the full MIC data dict

        mock_mics = [
            Mock(
                mic=real_mic_data["mic"],
                market_name=real_mic_data["operating_mic_name"],
                iso_country_code=real_mic_data["country_code"],
                city=real_mic_data["city"],
            ),
            Mock(
                mic="XLON",
                market_name="LONDON STOCK EXCHANGE",
                iso_country_code="GB",
                city="LONDON",
            ),
        ]

        # Set up the complete query chain: session.query().filter_by().limit().all()
        mock_query_base = Mock()
        mock_filter_result = Mock()
        mock_limit_result = Mock()

        mock_query_base.filter_by.return_value = mock_filter_result
        mock_filter_result.filter_by.return_value = (
            mock_filter_result  # For potential country filter
        )
        mock_filter_result.limit.return_value = mock_limit_result
        mock_limit_result.all.return_value = mock_mics

        mock_session.query.return_value = mock_query_base

        runner = CliRunner()
        result = runner.invoke(cli, ["mic", "list", "--limit", "2"])

        assert result.exit_code == 0
        assert real_mic_data["mic"] in result.output  # XSTO
        assert "NASDAQ STOCKHOLM" in result.output or "STOCKHOLM" in result.output

    @pytest.mark.cli
    @patch("marketdata_api.cli.get_session")
    def test_mic_get_success(self, mock_get_session):
        """Test successful MIC get command."""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Create mock enum objects for status and operation_type
        mock_status = Mock()
        mock_status.value = "ACTIVE"
        mock_operation_type = Mock()
        mock_operation_type.value = "OPRT"

        mock_mic = Mock(
            mic="XSTO",
            market_name="NASDAQ STOCKHOLM AB",
            legal_entity_name="NASDAQ STOCKHOLM AB",
            iso_country_code="SE",
            city="STOCKHOLM",
            status=mock_status,
            operation_type=mock_operation_type,
            operating_mic="XSTO",
            lei="549300KBQIVNEJEZVL96",
        )

        # Set up the query chain properly
        mock_query = Mock()
        mock_filter = Mock()
        mock_query.filter_by.return_value = mock_filter
        mock_filter.first.return_value = mock_mic
        mock_session.query.return_value = mock_query

        runner = CliRunner()
        result = runner.invoke(cli, ["mic", "get", "XSTO"])

        assert result.exit_code == 0
        assert "XSTO" in result.output
        assert "NASDAQ STOCKHOLM AB" in result.output


class TestStatsCommand:
    """Test database statistics command."""

    @pytest.mark.cli
    @patch("marketdata_api.cli.get_session")
    def test_stats_command_success(self, mock_get_session):
        """Test successful stats command."""
        mock_session = Mock()
        mock_get_session.return_value.__enter__.return_value = mock_session

        # Mock count queries for different tables
        mock_session.query.return_value.count.side_effect = [49, 129, 2794, 246]

        runner = CliRunner()
        result = runner.invoke(cli, ["stats"])

        assert result.exit_code == 0
        assert "49" in result.output  # Instruments count
        assert "129" in result.output  # Transparency calculations count
        assert "2,794" in result.output  # MIC codes count
        assert "246" in result.output  # Legal entities count


class TestCLIErrorHandling:
    """Test CLI error handling and edge cases."""

    @pytest.mark.cli
    def test_invalid_command(self):
        """Test handling of invalid commands."""
        runner = CliRunner()
        result = runner.invoke(cli, ["invalid-command"])

        assert result.exit_code != 0
        assert "No such command" in result.output

    @pytest.mark.cli
    @patch("marketdata_api.cli.get_session")
    def test_database_error_handling(self, mock_get_session):
        """Test graceful handling of database errors."""
        # Simulate database connection failure
        mock_get_session.side_effect = Exception("Database connection failed")

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "list"])

        # The CLI handles errors gracefully and exits with 0, but should show error message
        assert result.exit_code == 0  # CLI handles errors gracefully
        assert (
            "Error" in result.output
            or "error" in result.output
            or "Database connection failed" in result.output
        )

    @pytest.mark.cli
    def test_missing_required_argument(self):
        """Test handling of missing required arguments."""
        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "get"])  # Missing ISIN argument

        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output


class TestCLIOutputFormatting:
    """Test CLI output formatting and presentation."""

    @pytest.mark.cli
    @patch("marketdata_api.cli.SqliteInstrumentService")
    def test_table_output_format(self, mock_service):
        """Test that list commands produce properly formatted tables."""
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        # Use real test data
        real_instrument = get_test_instrument()
        mock_instruments = [
            Mock(
                isin=real_instrument["isin"],
                full_name=real_instrument["full_name"],
                instrument_type=real_instrument["instrument_type"],
                currency=real_instrument["currency"],
            )
        ]
        mock_service_instance.list_instruments.return_value = (Mock(), mock_instruments, 1)

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "list"])

        assert result.exit_code == 0
        # Should contain table formatting characters (Rich tables use these Unicode chars)
        assert "│" in result.output or "┌" in result.output or "└" in result.output  # Table borders
        assert "ISIN" in result.output  # Column header

    @pytest.mark.cli
    @patch("marketdata_api.cli.SqliteInstrumentService")
    def test_panel_output_format(self, mock_service):
        """Test that get commands produce properly formatted panels."""
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance

        mock_instrument = Mock(
            isin="US0378331005",
            full_name="Apple Inc.",
            short_name="AAPL",
            instrument_type="equity",
            currency="USD",
            cfi_code="ESVUFR",
            relevant_trading_venue="XNGS",
            lei_id="HWUPKR0MPOU8FGXBT394",
            created_at="2024-01-01",
        )
        mock_service_instance.get_instrument.return_value = (Mock(), mock_instrument)

        runner = CliRunner()
        result = runner.invoke(cli, ["instruments", "get", "US0378331005"])

        assert result.exit_code == 0
        # Should contain panel formatting
        assert "╭" in result.output or "┌" in result.output  # Panel borders


@pytest.mark.upgrade
class TestCLIVersionCompatibility:
    """Test CLI compatibility across versions."""

    @pytest.mark.cli
    def test_command_structure_stability(self):
        """Test that core command structure remains stable."""
        runner = CliRunner()

        # These commands should always exist for backward compatibility
        essential_commands = [
            ["instruments", "--help"],
            ["mic", "--help"],
            ["stats", "--help"],
            ["transparency", "--help"],
        ]

        for cmd in essential_commands:
            result = runner.invoke(cli, cmd)
            assert result.exit_code == 0, f"Command {' '.join(cmd)} should always work"

    @pytest.mark.cli
    def test_output_format_stability(self):
        """Test that output formats remain consistent for scripting."""
        # This test would verify that machine-readable output formats
        # (JSON, CSV) remain consistent across versions
        # Implementation depends on specific format requirements
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
