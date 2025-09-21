#!/usr/bin/env python3
"""
MarketDataAPI Professional CLI

A command-line interface for the MarketDataAPI using Click framework
for professional-grade CLI with proper command grouping, help, and error handling.

Install with: pip install -e .
Use with: marketdata instruments list
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Modern CLI framework
import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# MarketDataAPI imports - moved to top level for efficiency
try:
    from sqlalchemy.exc import OperationalError

    from marketdata_api.config import SQLITE_DB_PATH
    from marketdata_api.database.initialize_db import database_exists, init_database
    from marketdata_api.database.session import get_session
    from marketdata_api.models.sqlite.instrument import Instrument
    from marketdata_api.models.sqlite.legal_entity import LegalEntity
    from marketdata_api.models.sqlite.market_identification_code import (
        MarketIdentificationCode,
        MICStatus,
    )
    from marketdata_api.models.sqlite.transparency import TransparencyCalculation
    from marketdata_api.services.file_management_service import FileManagementService
    from marketdata_api.services.mic_data_loader import MICDataLoader, remote_mic_service
    from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
    from marketdata_api.services.sqlite.legal_entity_service import LegalEntityService
    from marketdata_api.services.sqlite.transparency_service import TransparencyService
except ImportError as e:
    print(f"Error importing MarketDataAPI modules: {e}")
    print("Make sure you're in the correct project directory and the API is installed.")
    sys.exit(1)

# Initialize Rich console for beautiful output
console = Console()


def check_database_initialized():
    """Check if database exists and offer to initialize it if not."""
    try:
        if not database_exists():
            console.print("\n[bold red]⚠️  Database not found![/bold red]")
            console.print(f"[dim]Expected location: {SQLITE_DB_PATH}[/dim]")
            console.print(
                "\n[yellow]The database needs to be initialized before using CLI commands.[/yellow]"
            )

            if click.confirm("Would you like to initialize a new database now?"):
                console.print("[cyan]Initializing database...[/cyan]")
                if init_database():
                    console.print("[green]✓ Database initialized successfully![/green]\n")
                    return True
                else:
                    console.print("[red]✗ Database initialization failed![/red]")
                    console.print(
                        "[dim]Run 'marketdata init --force' to try manual initialization.[/dim]"
                    )
                    return False
            else:
                console.print(
                    "\n[dim]To initialize manually, run: [bold]marketdata init[/bold][/dim]"
                )
                console.print(
                    "[dim]Or set custom database path with: [bold]SQLITE_DB_PATH=/path/to/db[/bold][/dim]"
                )
                return False
        return True
    except Exception as e:
        console.print(f"[red]Database check failed: {e}[/red]")
        return False


def handle_database_error(func):
    """Decorator to handle database connection errors gracefully."""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if "no such table" in str(e).lower():
                console.print(f"\n[red]Database Error:[/red] {str(e)}")
                console.print(
                    "\n[yellow]This usually means the database tables don't exist.[/yellow]"
                )
                if click.confirm("Would you like to initialize the database tables now?"):
                    if init_database():
                        console.print(
                            "[green]✓ Database initialized. Please retry your command.[/green]"
                        )
                    else:
                        console.print("[red]✗ Database initialization failed.[/red]")
                return
            else:
                console.print(f"\n[red]Database Error:[/red] {str(e)}")
                console.print("[dim]Check your database configuration and try again.[/dim]")
                return
        except Exception as e:
            console.print(f"[red]Error:[/red] {str(e)}")
            return

    return wrapper


# Custom Click group with better help formatting
class CustomGroup(click.Group):
    def format_help(self, ctx, formatter):
        """Custom help formatting with Rich styling"""
        console.print("\n[bold cyan]MarketDataAPI CLI[/bold cyan]")
        console.print("[dim]Professional command-line interface for financial market data[/dim]\n")
        super().format_help(ctx, formatter)


@click.group(cls=CustomGroup, invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--format", type=click.Choice(["table", "json", "csv"]), default="table", help="Output format"
)
@click.pass_context
def cli(ctx, verbose, format):
    """MarketDataAPI CLI - Professional financial data interface"""
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["format"] = format

    if ctx.invoked_subcommand is None:
        console.print(
            Panel.fit(
                "[bold green]MarketDataAPI Professional CLI[/bold green]\n\n"
                + "[cyan]Available Commands:[/cyan]\n"
                + "• [yellow]init[/yellow] - Initialize database (run this first!)\n"
                + "• [yellow]instruments[/yellow] - Manage financial instruments\n"
                + "• [yellow]transparency[/yellow] - Transparency calculations\n"
                + "• [yellow]mic[/yellow] - Market identification codes\n"
                + "• [yellow]entities[/yellow] - Legal entities\n"
                + "• [yellow]files[/yellow] - File management operations\n"
                + "• [yellow]stats[/yellow] - Database statistics\n"
                + "• [yellow]cfi[/yellow] - Comprehensive CFI code analysis\n\n"
                + "Use [green]--help[/green] with any command for details"
            )
        )


# ============================================================================
# INSTRUMENTS COMMAND GROUP
# ============================================================================


@cli.group()
def instruments():
    """Manage financial instruments (equities, bonds, derivatives, etc.)"""
    pass


@instruments.command()
@click.option("--type", help="Filter by instrument type")
@click.option("--currency", help="Filter by currency")
@click.option("--limit", default=20, help="Number of results to show")
@click.pass_context
def list(ctx, type, currency, limit):
    """List instruments with optional filtering"""
    try:
        with console.status("[bold green]Fetching instruments..."):
            with get_session() as session:
                query = session.query(Instrument)
                if type:
                    query = query.filter(Instrument.instrument_type == type)
                if currency:
                    query = query.filter(Instrument.currency == currency)

                # Execute query within session context
                instruments_data = []
                for inst in query.limit(limit).all():
                    instruments_data.append(
                        {
                            "isin": inst.isin,
                            "full_name": inst.full_name,
                            "instrument_type": inst.instrument_type,
                            "currency": inst.currency,
                        }
                    )

        if not instruments_data:
            console.print("[yellow]No instruments found[/yellow]")
            return

        # Rich table output
        table = Table(title=f"Instruments {f'({type})' if type else ''}")
        table.add_column("ISIN", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Type", style="magenta")
        table.add_column("Currency", style="yellow")

        for inst_data in instruments_data:
            table.add_row(
                inst_data["isin"] or "N/A",
                (inst_data["full_name"] or "N/A")[:50]
                + ("..." if len(inst_data["full_name"] or "") > 50 else ""),
                inst_data["instrument_type"] or "N/A",
                inst_data["currency"] or "N/A",
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(instruments_data)} instruments[/dim]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@instruments.command("get")
@click.argument("isin")
@click.pass_context
@handle_database_error
def get_instrument(ctx, isin):
    """Get detailed instrument information by ISIN"""
    try:
        service = SqliteInstrumentService()

        with console.status(f"[bold green]Looking up {isin}..."):
            session, instrument = service.get_instrument(isin)

        if not instrument:
            console.print(f"[red]Instrument not found: {isin}[/red]")
            return

        # Rich panel output
        details = f"""[cyan]ISIN:[/cyan] {instrument.isin}
[cyan]Name:[/cyan] {instrument.full_name or 'N/A'}
[cyan]Short Name:[/cyan] {instrument.short_name or 'N/A'}
[cyan]Type:[/cyan] {instrument.instrument_type or 'N/A'}
[cyan]Currency:[/cyan] {instrument.currency or 'N/A'}
[cyan]CFI Code:[/cyan] {instrument.cfi_code or 'N/A'}
[cyan]Trading Venue:[/cyan] {instrument.relevant_trading_venue or 'N/A'}
[cyan]LEI ID:[/cyan] {instrument.lei_id or 'N/A'}
[cyan]Created:[/cyan] {instrument.created_at or 'N/A'}"""

        console.print(Panel(details, title=f"Instrument Details: {isin}"))
        session.close()

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@instruments.command()
@click.argument("isin")
@click.argument("instrument_type", default="equity")
@click.pass_context
def create(ctx, isin, instrument_type):
    """Create instrument from external data sources (FIRDS)"""
    try:
        service = SqliteInstrumentService()

        with console.status(f"[bold green]Creating {instrument_type} instrument for {isin}..."):
            instrument = service.create_instrument(isin, instrument_type)

        if instrument:
            console.print(f"[green]✓[/green] Created instrument: {instrument.isin}")
            console.print(f"  ID: {instrument.id}")
            console.print(f"  Type: {instrument.instrument_type}")
        else:
            console.print(f"[red]Failed to create instrument: {isin}[/red]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@instruments.command()
@click.argument("isin")
@click.pass_context
def enrich(ctx, isin):
    """Enrich existing instrument with external data (FIGI, LEI, etc.)"""
    try:
        service = SqliteInstrumentService()

        # First get the instrument
        with console.status(f"[bold green]Looking up instrument {isin}..."):
            session, instrument = service.get_instrument(isin)

        if not instrument:
            console.print(f"[red]Instrument not found: {isin}[/red]")
            console.print("[yellow]Use 'instruments create' to create it first[/yellow]")
            return

        session.close()

        with console.status(f"[bold green]Enriching instrument {isin}..."):
            enriched_session, enriched_instrument = service.enrich_instrument(instrument)

        if enriched_instrument:
            console.print(f"[green]✓[/green] Enriched instrument: {enriched_instrument.isin}")

            # Show enrichment results
            enrichment_info = []
            if hasattr(enriched_instrument, "figi_mappings") and enriched_instrument.figi_mappings:
                enrichment_info.append("[green]FIGI data[/green]")
            if hasattr(enriched_instrument, "legal_entity") and enriched_instrument.legal_entity:
                enrichment_info.append("[green]Legal entity data[/green]")

            if enrichment_info:
                console.print(f"  Added: {', '.join(enrichment_info)}")
            else:
                console.print("  [yellow]No additional data found to enrich[/yellow]")
        else:
            console.print(f"[red]Failed to enrich instrument: {isin}[/red]")

        enriched_session.close()

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@instruments.command()
@click.option("--jurisdiction", default="SE", help="Filter by competent authority jurisdiction")
@click.option("--type", default="equity", help="Instrument type to create")
@click.option("--limit", type=int, help="Maximum number of instruments to create")
@click.option("--batch-size", default=10, help="Number of instruments per batch")
@click.option(
    "--skip-existing/--no-skip-existing", default=True, help="Skip instruments already in database"
)
@click.option("--enrichment/--no-enrichment", default=True, help="Enable FIGI/LEI enrichment")
@click.pass_context
def bulk_create(ctx, jurisdiction, type, limit, batch_size, skip_existing, enrichment):
    """Create multiple instruments in bulk with filtering"""
    try:
        service = SqliteInstrumentService()

        # Show configuration
        console.print(f"[cyan]Bulk Creation Configuration:[/cyan]")
        console.print(f"  Jurisdiction: [yellow]{jurisdiction}[/yellow]")
        console.print(f"  Type: [yellow]{type}[/yellow]")
        console.print(f"  Limit: [yellow]{limit or 'No limit'}[/yellow]")
        console.print(f"  Batch size: [yellow]{batch_size}[/yellow]")
        console.print(f"  Skip existing: [yellow]{skip_existing}[/yellow]")
        console.print(f"  Enrichment: [yellow]{enrichment}[/yellow]")
        console.print()

        with console.status("[bold green]Processing bulk instrument creation..."):
            results = service.create_instruments_bulk(
                jurisdiction=jurisdiction,
                instrument_type=type,
                limit=limit,
                skip_existing=skip_existing,
                enable_enrichment=enrichment,
                batch_size=batch_size,
            )

        # Display results
        console.print(f"[green]✓[/green] Bulk creation completed!")
        console.print()

        # Summary table
        summary_table = Table(title="Creation Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="green")
        summary_table.add_column("Details", style="yellow")

        summary_table.add_row(
            "Found", str(results["total_found"]), f"Matching {jurisdiction} {type} instruments"
        )
        summary_table.add_row(
            "Created", str(results["total_created"]), "Successfully created with venues"
        )
        summary_table.add_row("Failed", str(results["total_failed"]), "Creation errors")
        summary_table.add_row(
            "Time",
            f"{results['elapsed_time']:.1f}s",
            (
                f"Avg: {results['elapsed_time']/max(1, results['total_created']):.1f}s per instrument"
                if results["total_created"] > 0
                else ""
            ),
        )

        console.print(summary_table)

        # Show batch details if verbose
        if ctx.obj.get("verbose") and results["batch_results"]:
            console.print()
            batch_table = Table(title="Batch Results")
            batch_table.add_column("Batch", style="cyan")
            batch_table.add_column("Created", style="green")
            batch_table.add_column("Failed", style="red")
            batch_table.add_column("Time", style="yellow")

            for idx, batch in enumerate(results["batch_results"], 1):
                batch_table.add_row(
                    str(idx),
                    str(batch["created"]),
                    str(batch["failed"]),
                    f"{batch['elapsed_time']:.1f}s",
                )

            console.print(batch_table)

        # Show failed instruments if any
        if results["failed_instruments"]:
            console.print()
            console.print(f"[red]Failed Instruments ({len(results['failed_instruments'])}):[/red]")
            for failure in results["failed_instruments"][:5]:  # Show first 5
                console.print(f"  [red]•[/red] {failure['isin']}: {failure['error']}")
            if len(results["failed_instruments"]) > 5:
                console.print(f"  [dim]... and {len(results['failed_instruments']) - 5} more[/dim]")

        # Show sample created instruments
        if results["created_instruments"]:
            console.print()
            sample_size = min(5, len(results["created_instruments"]))
            console.print(
                f"[green]Sample Created Instruments ({sample_size}/{len(results['created_instruments'])}):[/green]"
            )
            for isin in results["created_instruments"][:sample_size]:
                console.print(f"  [green]✓[/green] {isin}")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@instruments.command()
@click.argument("identifier")
@click.option("--type", default="equity", help="Instrument type for venue lookup")
@click.pass_context
def venues(ctx, identifier, type):
    """Get trading venues for an instrument"""
    try:
        service = SqliteInstrumentService()

        with console.status(f"[bold green]Fetching venues for {identifier}..."):
            venues_data = service.get_instrument_venues(identifier, type)

        if not venues_data:
            console.print(f"[yellow]No venues found for {identifier}[/yellow]")
            return

        table = Table(title=f"Trading Venues for {identifier}")
        table.add_column("Venue ID", style="cyan")
        table.add_column("MIC Code", style="magenta")
        table.add_column("First Trade", style="green")
        table.add_column("Status", style="yellow")

        for venue in venues_data:
            table.add_row(
                venue.get("venue_id", "N/A"),
                venue.get("mic_code", "N/A"),
                venue.get("first_trade_date", "N/A"),
                venue.get("venue_status", "N/A"),
            )

        console.print(table)
        console.print(f"\n[dim]Found {len(venues_data)} venues[/dim]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# TRANSPARENCY COMMAND GROUP
# ============================================================================


@cli.group()
def transparency():
    """Manage transparency calculations and FITRS data"""
    pass


@transparency.command()
@click.option("--limit", default=20, help="Number of results")
@click.option("--offset", default=0, help="Results offset")
@click.option("--type", help="Filter by file type (e.g., FULECR_E, FULNCR_D)")
@click.option(
    "--liquidity",
    type=click.Choice(["true", "false", "liquid", "non-liquid"]),
    help="Filter by liquidity status (liquid includes actively traded instruments)",
)
@click.option(
    "--threshold", type=click.Choice(["LIS", "SSTI", "SMS"]), help="Filter by threshold type"
)
@click.option("--isin", help="Filter by specific ISIN")
@click.pass_context
def list(ctx, limit, offset, type, liquidity, threshold, isin):
    """List transparency calculations with advanced filtering"""
    try:
        with console.status("[bold green]Fetching transparency calculations..."):
            with get_session() as session:
                # Build query with filters
                query = session.query(TransparencyCalculation)

                # Apply filters
                if type:
                    query = query.filter(TransparencyCalculation.file_type.ilike(f"%{type}%"))
                if isin:
                    query = query.filter(TransparencyCalculation.isin == isin.upper())
                if liquidity:
                    if liquidity.lower() in ["true", "liquid"]:
                        # Include both explicit liquidity=True AND instruments with trading activity
                        query = query.filter(
                            (TransparencyCalculation.liquidity == True)
                            | (
                                (TransparencyCalculation.liquidity.is_(None))
                                & (
                                    (TransparencyCalculation.total_volume_executed > 0)
                                    | (TransparencyCalculation.total_transactions_executed > 0)
                                )
                            )
                        )
                    elif liquidity.lower() in ["false", "non-liquid"]:
                        query = query.filter(TransparencyCalculation.liquidity == False)
                if threshold:
                    # Check if there's a threshold_type field, otherwise search in related data
                    if hasattr(TransparencyCalculation, "threshold_type"):
                        query = query.filter(
                            TransparencyCalculation.threshold_type == threshold.upper()
                        )

                # Execute query and extract data within session context
                calculations_data = []
                for calc in query.limit(limit).offset(offset).all():
                    period = (
                        f"{calc.from_date} to {calc.to_date}"
                        if calc.from_date and calc.to_date
                        else "N/A"
                    )
                    # Smart liquidity display based on FITRS analysis
                    volume = calc.total_volume_executed or 0
                    transactions = calc.total_transactions_executed or 0
                    has_trading_activity = volume > 0 or transactions > 0

                    if calc.liquidity is True:
                        liquidity_status = "✓ Liquid"
                    elif calc.liquidity is False:
                        liquidity_status = "✗ Non-Liquid"
                    elif has_trading_activity:
                        # FULECR_E files with missing Lqdty but trading activity = likely liquid
                        liquidity_status = "🔄 Active"
                    else:
                        liquidity_status = "❓ Unknown"

                    # Format volume
                    volume = "N/A"
                    if calc.total_volume_executed is not None:
                        if calc.total_volume_executed >= 1_000_000:
                            volume = f"{calc.total_volume_executed/1_000_000:.1f}M"
                        elif calc.total_volume_executed >= 1_000:
                            volume = f"{calc.total_volume_executed/1_000:.1f}K"
                        else:
                            volume = f"{calc.total_volume_executed:.0f}"

                    # Format transactions
                    transactions = "N/A"
                    if calc.total_transactions_executed is not None:
                        if calc.total_transactions_executed >= 1_000_000:
                            transactions = f"{calc.total_transactions_executed/1_000_000:.1f}M"
                        elif calc.total_transactions_executed >= 1_000:
                            transactions = f"{calc.total_transactions_executed/1_000:.1f}K"
                        else:
                            transactions = f"{calc.total_transactions_executed:,}"

                    # Extract additional data from raw_data JSON if available
                    raw_data = calc.raw_data or {}
                    instrument_class = raw_data.get("FinInstrmClssfctn", "N/A")
                    methodology = raw_data.get("Mthdlgy", "N/A")

                    calculations_data.append(
                        {
                            "id": str(calc.id)[:8] + "...",
                            "isin": calc.isin or "N/A",
                            "file_type": calc.file_type or "N/A",
                            "period": period,
                            "liquidity": liquidity_status,
                            "volume": volume,
                            "transactions": transactions,
                            "instrument_class": instrument_class,
                            "methodology": methodology,
                        }
                    )

        if not calculations_data:
            console.print("[yellow]No transparency calculations found[/yellow]")
            return

        # Create enhanced table
        title = "Transparency Calculations"
        if type or liquidity or threshold or isin:
            filters = []
            if type:
                filters.append(f"type:{type}")
            if liquidity:
                filters.append(f"liquidity:{liquidity}")
            if threshold:
                filters.append(f"threshold:{threshold}")
            if isin:
                filters.append(f"isin:{isin}")
            title += f" (filtered: {', '.join(filters)})"

        table = Table(title=title)
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("ISIN", style="green", no_wrap=True)
        table.add_column("Type", style="magenta", no_wrap=True)
        table.add_column("Period", style="yellow")
        table.add_column("Liquidity", style="red")
        table.add_column("Volume", style="blue", justify="right")
        table.add_column("Transactions", style="bright_blue", justify="right")
        table.add_column("Instrument", style="white", no_wrap=True)
        table.add_column("Method", style="bright_black", no_wrap=True)

        for calc_data in calculations_data:
            table.add_row(
                calc_data["id"],
                calc_data["isin"],
                calc_data["file_type"],
                calc_data["period"],
                calc_data["liquidity"],
                calc_data["volume"],
                calc_data["transactions"],
                calc_data["instrument_class"],
                calc_data["methodology"],
            )

        console.print(table)
        console.print(
            f"\n[dim]Showing {len(calculations_data)} calculations (offset: {offset})[/dim]"
        )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@transparency.command()
@click.argument("isin")
@click.option("--type", help="Instrument type (optional, will use database value if available)")
@click.pass_context
def create(ctx, isin, type):
    """Create transparency calculations for an ISIN from FITRS data"""
    try:
        service = TransparencyService()

        with console.status(f"[bold green]Creating transparency calculations for {isin}..."):
            calculations = service.create_transparency(isin, type)

        if not calculations:
            console.print(f"[yellow]No transparency data found in FITRS files for {isin}[/yellow]")
            return

        console.print(
            f"[green]✓[/green] Created {len(calculations)} transparency calculations for {isin}"
        )

        # Show created calculations
        table = Table(title=f"Created Transparency Calculations for {isin}")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("File Type", style="magenta")
        table.add_column("Period", style="yellow")
        table.add_column("Liquid", style="green")
        table.add_column("Transactions", style="blue")

        for calc in calculations:
            period = (
                f"{calc.from_date} to {calc.to_date}" if calc.from_date and calc.to_date else "N/A"
            )
            liquidity = "✓" if calc.liquidity else "✗"
            transactions = (
                f"{calc.total_transactions_executed:,}"
                if calc.total_transactions_executed
                else "N/A"
            )

            table.add_row(
                str(calc.id)[:8] + "...", calc.file_type or "N/A", period, liquidity, transactions
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@transparency.command("get")
@click.argument("isin")
@click.pass_context
def get_transparency(ctx, isin):
    """Get transparency calculations by ISIN"""
    try:
        service = TransparencyService()

        with console.status(f"[bold green]Looking up transparency calculations for {isin}..."):
            calculations = service.get_transparency_by_isin(isin.upper())

        if not calculations:
            console.print(f"[red]No transparency calculations found for ISIN: {isin}[/red]")
            return

        console.print(
            f"\n[bold]Found {len(calculations)} transparency calculation(s) for {isin}:[/bold]\n"
        )

        for i, calculation in enumerate(calculations, 1):
            # Handle None values safely
            from_date = calculation.from_date or "N/A"
            to_date = calculation.to_date or "N/A"
            transactions = (
                calculation.total_transactions_executed
                if calculation.total_transactions_executed is not None
                else 0
            )
            volume = (
                calculation.total_volume_executed
                if calculation.total_volume_executed is not None
                else 0
            )

            # Common details
            details = f"""[cyan]ID:[/cyan] {calculation.id or 'N/A'}
[cyan]ISIN:[/cyan] {calculation.isin or 'N/A'}
[cyan]File Type:[/cyan] {calculation.file_type or 'N/A'}
[cyan]Source File:[/cyan] {calculation.source_file or 'N/A'}
[cyan]Period:[/cyan] {from_date} to {to_date}
[cyan]Liquidity:[/cyan] {'Yes' if calculation.liquidity else 'No' if calculation.liquidity is not None else 'Unknown'}
[cyan]Transactions:[/cyan] {transactions:,}
[cyan]Volume:[/cyan] {volume:,.2f}
[cyan]Tech Record ID:[/cyan] {calculation.tech_record_id or 'N/A'}
[cyan]Created:[/cyan] {calculation.created_at or 'N/A'}"""

            # Add asset-type-specific details from raw_data
            raw_data = calculation.raw_data or {}

            # Check if this is equity data (FULECR files)
            is_equity = calculation.file_type and calculation.file_type.startswith("FULECR")

            if is_equity:
                # Equity-specific fields
                details += f"""

[yellow]📊 EQUITY-SPECIFIC DATA:[/yellow]
[cyan]Primary ID (ISIN):[/cyan] {raw_data.get('Id', 'N/A')}
[cyan]Secondary ID (Venue):[/cyan] {raw_data.get('Id_2', 'N/A')}
[cyan]Methodology:[/cyan] {raw_data.get('Mthdlgy', 'N/A')}
[cyan]Average Daily Turnover:[/cyan] {raw_data.get('AvrgDalyTrnvr', 'N/A')}
[cyan]Large in Scale:[/cyan] {raw_data.get('LrgInScale', 'N/A')}
[cyan]Avg Daily No. of Transactions:[/cyan] {raw_data.get('AvrgDalyNbOfTxs', 'N/A')}
[cyan]Avg Daily No. of Transactions (2nd):[/cyan] {raw_data.get('AvrgDalyNbOfTxs_2', 'N/A')}
[cyan]Average Transaction Value:[/cyan] {raw_data.get('AvrgTxVal', 'N/A')}
[cyan]Standard Market Size:[/cyan] {raw_data.get('StdMktSz', 'N/A')}
[cyan]Statistics:[/cyan] {raw_data.get('Sttstcs', 'N/A')}"""
            else:
                # Non-equity specific fields (FULNCR files)
                details += f"""

[yellow]📋 NON-EQUITY DATA:[/yellow]
[cyan]Description:[/cyan] {raw_data.get('Desc', 'N/A')}
[cyan]Classification:[/cyan] {raw_data.get('FinInstrmClssfctn', 'N/A')}"""

                # Show criteria fields (up to 7 for futures)
                for j in range(1, 8):
                    crit_name_key = f"CritNm_{j}" if j > 1 else "CritNm"
                    crit_val_key = f"CritVal_{j}" if j > 1 else "CritVal"

                    crit_name = raw_data.get(crit_name_key)
                    crit_val = raw_data.get(crit_val_key)

                    if crit_name or crit_val:
                        details += f"""
[cyan]Criterion {j}:[/cyan] {crit_name or 'N/A'} = {crit_val or 'N/A'}"""

            console.print(
                Panel(
                    details, title=f"[bold]Transparency Calculation {i}[/bold]", border_style="cyan"
                )
            )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@transparency.command()
@click.option("--limit", type=int, help="Maximum number of instruments to process")
@click.option("--batch-size", default=10, help="Number of instruments per batch")
@click.option(
    "--skip-existing/--no-skip-existing",
    default=True,
    help="Skip instruments that already have transparency data",
)
@click.pass_context
def bulk_create(ctx, limit, batch_size, skip_existing):
    """Create transparency calculations in bulk for instruments without them"""
    try:
        service = TransparencyService()

        # Show configuration
        console.print(f"[cyan]Bulk Transparency Creation Configuration:[/cyan]")
        console.print(f"  Limit: [yellow]{limit or 'No limit'}[/yellow]")
        console.print(f"  Batch size: [yellow]{batch_size}[/yellow]")
        console.print(f"  Skip existing: [yellow]{skip_existing}[/yellow]")
        console.print()

        with console.status("[bold green]Processing bulk transparency creation..."):
            results = service.create_transparency_bulk(
                limit=limit, batch_size=batch_size, skip_existing=skip_existing
            )

        # Display results
        console.print(f"[green]✓[/green] Bulk transparency creation completed!")
        console.print()

        # Summary table
        summary_table = Table(title="Creation Summary")
        summary_table.add_column("Metric", style="cyan")
        summary_table.add_column("Count", style="green")
        summary_table.add_column("Details", style="yellow")

        summary_table.add_row(
            "Instruments Found",
            str(results["total_instruments"]),
            "Instruments needing transparency calculations",
        )
        summary_table.add_row(
            "Processed", str(results["total_processed"]), "Instruments actually processed"
        )
        summary_table.add_row(
            "Calculations Created",
            str(results["total_created_calculations"]),
            "New transparency calculations",
        )
        summary_table.add_row("Skipped", str(results["total_skipped"]), "No FITRS data found")
        summary_table.add_row("Failed", str(results["total_failed"]), "Processing errors")
        summary_table.add_row(
            "Time",
            f"{results['elapsed_time']:.1f}s",
            (
                f"Avg: {results['elapsed_time']/max(1, results['total_processed']):.1f}s per instrument"
                if results["total_processed"] > 0
                else ""
            ),
        )

        console.print(summary_table)

        # Show batch details if verbose
        if ctx.obj.get("verbose") and results["batch_results"]:
            console.print()
            batch_table = Table(title="Batch Results")
            batch_table.add_column("Batch", style="cyan")
            batch_table.add_column("Processed", style="green")
            batch_table.add_column("Created", style="blue")
            batch_table.add_column("Failed", style="red")
            batch_table.add_column("Time", style="yellow")

            for idx, batch in enumerate(results["batch_results"], 1):
                batch_table.add_row(
                    str(idx),
                    str(batch["processed"]),
                    str(batch["created_calculations"]),
                    str(batch["failed"]),
                    f"{batch['elapsed_time']:.1f}s",
                )

            console.print(batch_table)

        # Show failed instruments if any
        if results["failed_instruments"]:
            console.print()
            console.print(f"[red]Failed Instruments ({len(results['failed_instruments'])}):[/red]")
            for failure in results["failed_instruments"][:5]:  # Show first 5
                console.print(f"  [red]•[/red] {failure['isin']}: {failure['error']}")
            if len(results["failed_instruments"]) > 5:
                console.print(f"  [dim]... and {len(results['failed_instruments']) - 5} more[/dim]")

        # Show successful instruments if any
        if results["successful_instruments"]:
            console.print()
            sample_size = min(5, len(results["successful_instruments"]))
            console.print(
                f"[green]Sample Successful Instruments ({sample_size}/{len(results['successful_instruments'])}):[/green]"
            )
            for success in results["successful_instruments"][:sample_size]:
                console.print(
                    f"  [green]✓[/green] {success['isin']}: {success['calculations_created']} calculations"
                )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# MIC COMMAND GROUP
# ============================================================================


@cli.group()
def mic():
    """Market Identification Code operations"""
    pass


@mic.command()
@click.option("--country", help="Filter by country code")
@click.option("--limit", default=20, help="Number of results")
@click.pass_context
def list(ctx, country, limit):
    """List MIC codes with optional filtering"""
    try:
        with console.status("[bold green]Fetching MIC codes..."):
            with get_session() as session:
                query = session.query(MarketIdentificationCode).filter_by(status=MICStatus.ACTIVE)
                if country:
                    query = query.filter_by(iso_country_code=country.upper())

                # Extract data within session context
                mics_data = []
                for mic in query.limit(limit).all():
                    mics_data.append(
                        {
                            "mic": mic.mic,
                            "market_name": mic.market_name,
                            "iso_country_code": mic.iso_country_code,
                            "city": mic.city,
                        }
                    )

        if not mics_data:
            console.print("[yellow]No MIC codes found[/yellow]")
            return

        table = Table(title=f"MIC Codes{f' for {country.upper()}' if country else ''}")
        table.add_column("MIC", style="cyan", no_wrap=True)
        table.add_column("Market Name", style="green")
        table.add_column("Country", style="magenta")
        table.add_column("City", style="yellow")

        for mic_data in mics_data:
            table.add_row(
                mic_data["mic"],
                (mic_data["market_name"] or "N/A")[:40]
                + ("..." if len(mic_data["market_name"] or "") > 40 else ""),
                mic_data["iso_country_code"] or "N/A",
                mic_data["city"] or "N/A",
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(mics_data)} MIC codes[/dim]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@mic.command("get")
@click.argument("mic_code")
@click.pass_context
def get_mic(ctx, mic_code):
    """Get detailed MIC information"""
    try:
        with console.status(f"[bold green]Looking up MIC {mic_code}..."):
            with get_session() as session:
                mic = (
                    session.query(MarketIdentificationCode).filter_by(mic=mic_code.upper()).first()
                )

                if not mic:
                    console.print(f"[red]MIC not found: {mic_code}[/red]")
                    return

                # Extract all data while session is active
                mic_data = {
                    "mic": mic.mic,
                    "market_name": mic.market_name,
                    "legal_entity_name": mic.legal_entity_name,
                    "iso_country_code": mic.iso_country_code,
                    "city": mic.city,
                    "status": mic.status.value if mic.status else "N/A",
                    "operation_type": mic.operation_type.value if mic.operation_type else "N/A",
                    "operating_mic": mic.operating_mic,
                    "lei": mic.lei,
                }

        details = f"""[cyan]MIC:[/cyan] {mic_data['mic']}
[cyan]Market Name:[/cyan] {mic_data['market_name']}
[cyan]Legal Entity:[/cyan] {mic_data['legal_entity_name'] or 'N/A'}
[cyan]Country:[/cyan] {mic_data['iso_country_code']}
[cyan]City:[/cyan] {mic_data['city'] or 'N/A'}
[cyan]Status:[/cyan] {mic_data['status']}
[cyan]Type:[/cyan] {mic_data['operation_type']}
[cyan]Operating MIC:[/cyan] {mic_data['operating_mic'] or 'N/A'}
[cyan]LEI:[/cyan] {mic_data['lei'] or 'N/A'}"""

        console.print(Panel(details, title=f"MIC Details: {mic_code.upper()}"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# Remote MIC subcommand group
@mic.group()
def remote():
    """Real-time MIC operations using official ISO registry"""
    pass


@remote.command()
@click.argument("mic_code")
@click.pass_context
def lookup(ctx, mic_code):
    """Look up MIC from official ISO registry"""
    try:
        with console.status(f"[bold green]Looking up {mic_code} from ISO registry..."):
            result = remote_mic_service.lookup_mic(mic_code.upper())

        if not result:
            console.print(f"[red]MIC {mic_code} not found in official registry[/red]")
            return

        details = f"""[cyan]MIC:[/cyan] {result.get('mic', 'N/A')}
[cyan]Market Name:[/cyan] {result.get('market_name', 'N/A')}
[cyan]Legal Entity:[/cyan] {result.get('legal_entity_name', 'N/A')}
[cyan]Country:[/cyan] {result.get('iso_country_code', 'N/A')}
[cyan]City:[/cyan] {result.get('city', 'N/A')}
[cyan]Status:[/cyan] {result.get('status', 'N/A')}
[cyan]Type:[/cyan] {result.get('oprt_sgmt', 'N/A')}"""

        console.print(Panel(details, title=f"Official MIC Data: {mic_code.upper()}"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# FIGI COMMAND GROUP
# ============================================================================


@cli.group()
def figi():
    """FIGI (Financial Instrument Global Identifier) operations"""
    pass


@figi.command("get")
@click.argument("isin")
@click.pass_context
def get_figi(ctx, isin):
    """Get FIGI mappings for an ISIN"""
    try:
        service = SqliteInstrumentService()
        session, instrument = service.get_instrument(isin)

        if not instrument:
            console.print(f"[red]No instrument found for ISIN: {isin}[/red]")
            return

        if not instrument.figi_mappings:
            console.print(f"[yellow]No FIGI mappings found for ISIN: {isin}[/yellow]")
            console.print(
                "Run '[cyan]marketdata instruments enrich {isin}[/cyan]' to fetch FIGI data"
            )
            return

        # Create table for FIGI data
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("FIGI", style="cyan")
        table.add_column("Composite FIGI", style="blue")
        table.add_column("Share Class FIGI", style="green")
        table.add_column("Ticker", style="yellow")
        table.add_column("Security Type", style="white")
        table.add_column("Market Sector", style="bright_black")

        for figi_mapping in instrument.figi_mappings:
            table.add_row(
                figi_mapping.figi or "N/A",
                figi_mapping.composite_figi or "N/A",
                figi_mapping.share_class_figi or "N/A",
                figi_mapping.ticker or "N/A",
                figi_mapping.security_type or "N/A",
                figi_mapping.market_sector or "N/A",
            )

        console.print(f"\n[bold]FIGI Mappings for {isin}[/bold]")
        console.print(f"Found {len(instrument.figi_mappings)} FIGI mapping(s)")
        console.print(table)

        session.close()

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@figi.command()
@click.argument("isin")
@click.option("--mic", help="MIC code to use for search (if available from venues)")
@click.pass_context
def search(ctx, isin, mic):
    """Search for FIGI data using the enhanced OpenFIGI service"""
    try:
        from marketdata_api.services.openfigi import OpenFIGIService

        openfigi_service = OpenFIGIService()

        console.print(f"[cyan]Searching OpenFIGI for ISIN: {isin}[/cyan]")
        if mic:
            console.print(f"[cyan]Using MIC code: {mic}[/cyan]")

        # Search for FIGIs
        figi_results, search_strategy = openfigi_service.search_figi(isin, mic)

        if not figi_results:
            console.print(f"[yellow]No FIGI data found for ISIN: {isin}[/yellow]")
            if mic:
                console.print("[yellow]Try searching without MIC code for broader results[/yellow]")
            return

        # Create table for search results
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("FIGI", style="cyan")
        table.add_column("Name", style="white")
        table.add_column("Ticker", style="yellow")
        table.add_column("Exchange", style="blue")
        table.add_column("Security Type", style="green")
        table.add_column("Market Sector", style="bright_black")

        for result in figi_results:
            table.add_row(
                getattr(result, "figi", "N/A") or "N/A",
                getattr(result, "name", "N/A") or "N/A",
                getattr(result, "ticker", "N/A") or "N/A",
                getattr(result, "exch_code", "N/A") or "N/A",
                getattr(result, "security_type", "N/A") or "N/A",
                getattr(result, "market_sector", "N/A") or "N/A",
            )

        console.print(f"\n[bold]OpenFIGI Search Results for {isin}[/bold]")
        console.print(f"Found {len(figi_results)} FIGI(s)")
        console.print(table)

        # Show strategy used
        strategy_messages = {
            "mic_specific": f"[green]✓ Used MIC-specific search with {mic}[/green]",
            "broad_search": "[blue]ℹ Used ISIN-only broad search (MIC-specific failed)[/blue]",
            "no_results": "[red]❌ Both search strategies failed[/red]",
        }
        console.print(
            strategy_messages.get(search_strategy, f"[yellow]Strategy: {search_strategy}[/yellow]")
        )

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# LEGAL ENTITIES COMMAND GROUP
# ============================================================================


@cli.group()
def entities():
    """Legal entity operations"""
    pass


@entities.command()
@click.option("--limit", default=20, help="Number of results to show")
@click.option("--status", help="Filter by entity status")
@click.option("--jurisdiction", help="Filter by jurisdiction")
@click.pass_context
def list(ctx, limit, status, jurisdiction):
    """List legal entities with optional filtering"""
    try:
        with console.status("[bold green]Fetching legal entities..."):
            with get_session() as session:
                query = session.query(LegalEntity)
                if status:
                    query = query.filter(LegalEntity.status == status.upper())
                if jurisdiction:
                    query = query.filter(LegalEntity.jurisdiction == jurisdiction.upper())

                # Execute query within session context
                entities_data = []
                for entity in query.limit(limit).all():
                    entities_data.append(
                        {
                            "lei": entity.lei,
                            "name": entity.name,
                            "status": entity.status,
                            "jurisdiction": entity.jurisdiction,
                            "legal_form": entity.legal_form,
                        }
                    )

        if not entities_data:
            console.print("[yellow]No legal entities found[/yellow]")
            return

        # Rich table output
        table = Table(title=f"Legal Entities {f'({status})' if status else ''}")
        table.add_column("LEI", style="cyan", no_wrap=True)
        table.add_column("Name", style="green")
        table.add_column("Status", style="magenta")
        table.add_column("Jurisdiction", style="yellow")
        table.add_column("Legal Form", style="blue")

        for entity_data in entities_data:
            table.add_row(
                (
                    entity_data["lei"][:20] + "..."
                    if len(entity_data["lei"]) > 20
                    else entity_data["lei"]
                ),
                (entity_data["name"] or "N/A")[:30]
                + ("..." if len(entity_data["name"] or "") > 30 else ""),
                entity_data["status"] or "N/A",
                entity_data["jurisdiction"] or "N/A",
                (entity_data["legal_form"] or "N/A")[:20]
                + ("..." if len(entity_data["legal_form"] or "") > 20 else ""),
            )

        console.print(table)
        console.print(f"\n[dim]Showing {len(entities_data)} legal entities[/dim]")

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@entities.command("get")
@click.argument("lei")
@click.pass_context
def get_entity(ctx, lei):
    """Get legal entity information by LEI"""
    try:
        service = LegalEntityService()

        with console.status(f"[bold green]Looking up entity {lei}..."):
            session, entity = service.get_entity(lei)

        if not entity:
            console.print(f"[red]Legal entity not found: {lei}[/red]")
            return

        details = f"""[cyan]LEI:[/cyan] {entity.lei}
[cyan]Name:[/cyan] {entity.name}
[cyan]Registered As:[/cyan] {entity.registered_as or 'N/A'}
[cyan]Legal Form:[/cyan] {entity.legal_form or 'N/A'}
[cyan]Status:[/cyan] {entity.status or 'N/A'}
[cyan]Jurisdiction:[/cyan] {entity.jurisdiction or 'N/A'}
[cyan]BIC:[/cyan] {entity.bic or 'N/A'}
[cyan]Managing LOU:[/cyan] {entity.managing_lou or 'N/A'}
[cyan]Registration Status:[/cyan] {entity.registration_status or 'N/A'}"""

        console.print(Panel(details, title=f"Legal Entity: {lei}"))
        session.close()

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# FILE MANAGEMENT COMMANDS
# ============================================================================


@cli.group()
@click.pass_context
def files(ctx):
    """File management operations - download, list, cleanup ESMA files"""
    pass


@files.command("list")
@click.option(
    "--file-type",
    type=click.Choice(["firds", "fitrs", "all"]),
    default="all",
    help="Filter by file type",
)
@click.option("--date-from", help="Filter from date (YYYY-MM-DD)")
@click.option("--date-to", help="Filter to date (YYYY-MM-DD)")
@click.option("--limit", type=int, default=50, help="Limit number of results")
@click.pass_context
def list_files(ctx, file_type, date_from, date_to, limit):
    """List available files with filtering options"""
    try:
        file_service = FileManagementService()

        with console.status("[bold green]Loading files..."):
            if file_type == "all":
                all_files_dict = file_service.get_all_files()
                # Flatten the dictionary to a list
                files_data = []
                for file_list in all_files_dict.values():
                    files_data.extend(file_list)
            else:
                files_data = file_service.get_files_with_filters(
                    file_type=file_type, date_from=date_from, date_to=date_to, limit=limit
                )

        if not files_data:
            console.print("[yellow]No files found matching criteria[/yellow]")
            return

        # Apply limit if specified
        if limit and len(files_data) > limit:
            files_data = files_data[:limit]

        # Create Rich table
        table = Table(title=f"Local Files ({len(files_data)} total)")
        table.add_column("Filename", style="cyan", overflow="fold")
        table.add_column("Type", style="magenta")
        table.add_column("Dataset", style="blue")
        table.add_column("Size", style="yellow")
        table.add_column("Modified", style="green")

        for file_info in files_data:
            # Format file size
            size_mb = file_info.size / (1024 * 1024) if file_info.size else 0
            size_str = f"{size_mb:.1f} MB" if size_mb > 0 else "N/A"

            # Format date
            modified_str = (
                file_info.modified.strftime("%Y-%m-%d %H:%M") if file_info.modified else "N/A"
            )

            table.add_row(
                file_info.name,
                file_info.file_type,
                file_info.dataset_type or "N/A",
                size_str,
                modified_str,
            )

        console.print(table)

        # Summary info
        total_size_mb = sum(f.size for f in files_data if f.size) / (1024 * 1024)
        console.print(f"[dim]Total size: {total_size_mb:.1f} MB[/dim]")

    except Exception as e:
        console.print(f"[red]Error listing files: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@files.command("download")
@click.argument("file_type", type=click.Choice(["firds", "fitrs"]))
@click.option("--date", help="Specific date to download (YYYY-MM-DD)")
@click.option(
    "--dataset",
    help="Dataset type (e.g., FULINS_E for equity, FULINS_D for debt, FULINS_S, FULINS_R, etc.)",
)
@click.option("--force", is_flag=True, help="Force re-download even if file exists")
@click.pass_context
def download_files(ctx, file_type, date, dataset, force):
    """Download ESMA files (FIRDS or FITRS) with optional dataset filtering"""
    try:
        file_service = FileManagementService()

        if date:
            console.print(f"[cyan]Downloading {file_type.upper()} files for {date}...[/cyan]")
        else:
            console.print(f"[cyan]Downloading latest {file_type.upper()} files...[/cyan]")

        with console.status("[bold green]Downloading and processing..."):
            result = file_service.download_by_criteria(
                file_type=file_type, date=date, dataset=dataset, force_update=force
            )

        if result.get("success"):
            console.print(f"[green]✓ Download completed successfully![/green]")
            console.print(f"[dim]{result.get('message', '')}[/dim]")

            # Show summary of downloaded files
            downloaded = result.get("files_downloaded", [])
            skipped = result.get("files_skipped", [])
            failed = result.get("files_failed", [])

            if downloaded:
                table = Table(title="Downloaded Files")
                table.add_column("Filename", style="cyan")
                table.add_column("Status", style="green")

                for file_info in downloaded:
                    table.add_row(file_info.get("filename", str(file_info)), "✓ Downloaded")
                console.print(table)

            if skipped:
                console.print(f"[yellow]⚠ Skipped {len(skipped)} files (already exist)[/yellow]")

            if failed:
                console.print(f"[red]✗ Failed to download {len(failed)} files[/red]")
                for failed_file in failed[:3]:  # Show first 3 failures
                    console.print(f"  [red]• {failed_file}[/red]")
        else:
            console.print(f"[red]✗ Download failed: {result.get('message', 'Unknown error')}[/red]")

    except Exception as e:
        console.print(f"[red]Error downloading files: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@files.command("delete")
@click.argument("filename")
@click.option("--confirm", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
def delete_file(ctx, filename, confirm):
    """Delete a specific file"""
    try:
        if not confirm:
            if not click.confirm(f"Are you sure you want to delete '{filename}'?"):
                console.print("[yellow]Operation cancelled[/yellow]")
                return

        file_service = FileManagementService()

        with console.status("[bold red]Deleting file..."):
            result = file_service.delete_file(filename)

        if result.get("success"):
            console.print(f"[green]✓ File '{filename}' deleted successfully[/green]")
        else:
            console.print(
                f"[red]✗ Failed to delete file: {result.get('message', 'Unknown error')}[/red]"
            )

    except Exception as e:
        console.print(f"[red]Error deleting file: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@files.command("cleanup")
@click.option(
    "--dry-run", is_flag=True, help="Show what would be deleted without actually deleting"
)
@click.option("--older-than", type=int, default=30, help="Delete files older than N days")
@click.pass_context
def cleanup_files(ctx, dry_run, older_than):
    """Clean up old files based on retention policies"""
    try:
        file_service = FileManagementService()

        mode_text = "DRY RUN - " if dry_run else ""
        console.print(f"[cyan]{mode_text}Cleaning up files older than {older_than} days...[/cyan]")

        with console.status("[bold yellow]Scanning for old files..."):
            result = file_service.auto_cleanup_outdated_patterns(
                days_to_keep=older_than, dry_run=dry_run
            )

        if result.get("success"):
            cleaned_files = result.get("cleaned_files", [])

            if cleaned_files:
                table = Table(title=f"{'Files to Delete' if dry_run else 'Deleted Files'}")
                table.add_column("Filename", style="red")
                table.add_column("Age (days)", style="yellow")
                table.add_column("Size", style="cyan")

                for file_info in cleaned_files:
                    table.add_row(
                        file_info.get("filename", "N/A"),
                        str(file_info.get("age_days", "N/A")),
                        file_info.get("size", "N/A"),
                    )
                console.print(table)

                action_text = "would be deleted" if dry_run else "deleted"
                console.print(f"[green]✓ {len(cleaned_files)} files {action_text}[/green]")
            else:
                console.print("[green]✓ No old files found - nothing to clean up[/green]")
        else:
            console.print(f"[red]✗ Cleanup failed: {result.get('message', 'Unknown error')}[/red]")

    except Exception as e:
        console.print(f"[red]Error during cleanup: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@files.command("stats")
@click.pass_context
def file_stats(ctx):
    """Show file storage statistics"""
    try:
        file_service = FileManagementService()

        with console.status("[bold green]Gathering file statistics..."):
            stats = file_service.get_storage_stats()

        if stats:
            # Main statistics panel
            stats_text = f"""[cyan]Total Files:[/cyan] {stats.get('total_files', 0):,}
[cyan]Total Size:[/cyan] {stats.get('total_size_gb', 0):.2f} GB
[cyan]Available Space:[/cyan] {stats.get('available_space_gb', 0):.2f} GB
[cyan]FIRDS Files:[/cyan] {stats.get('firds_count', 0):,}
[cyan]FITRS Files:[/cyan] {stats.get('fitrs_count', 0):,}"""

            console.print(Panel(stats_text, title="File Storage Statistics"))

            # File type breakdown if available
            if "file_types" in stats:
                table = Table(title="File Type Breakdown")
                table.add_column("Type", style="magenta")
                table.add_column("Count", style="green")
                table.add_column("Size (MB)", style="yellow")

                for file_type, type_stats in stats["file_types"].items():
                    table.add_row(
                        file_type,
                        str(type_stats.get("count", 0)),
                        f"{type_stats.get('size_mb', 0):.1f}",
                    )
                console.print(table)
        else:
            console.print("[yellow]Unable to retrieve file statistics[/yellow]")

    except Exception as e:
        console.print(f"[red]Error getting file statistics: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@files.command("available")
@click.argument("file_type", type=click.Choice(["firds", "fitrs"]))
@click.option("--days", type=int, default=7, help="Check availability for last N days")
@click.option(
    "--dataset",
    help="Filter by dataset type (e.g., FULINS_E for equity, FULINS_D for debt, FULINS_S, FULINS_R, etc.)",
)
@click.pass_context
def available_files(ctx, file_type, days, dataset):
    """Check what files are available for download from ESMA with optional dataset filtering"""
    try:
        from datetime import datetime, timedelta

        # Calculate date range
        date_to = datetime.now().strftime("%Y-%m-%d")
        date_from = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        file_service = FileManagementService()

        with console.status(f"[bold green]Checking available {file_type.upper()} files..."):
            # Handle dataset filtering differently for FIRDS vs FITRS
            asset_type = None
            file_type_filter = None

            if dataset:
                if file_type.lower() == "firds" and "FULINS_" in dataset:
                    # For FIRDS: extract asset type (e.g., FULINS_E -> E)
                    asset_type = dataset.split("_")[1]
                elif file_type.lower() == "fitrs":
                    # For FITRS: use the dataset as a file type filter
                    # FULECR_E should match FULECR files with _E_ pattern
                    if "_" in dataset:
                        prefix, suffix = dataset.split("_", 1)
                        if prefix in ["FULECR", "FULNCR"]:
                            file_type_filter = prefix
                            asset_type = suffix
                        else:
                            # If it's something like FULINS_E, extract the asset type
                            asset_type = suffix

            available = file_service.get_available_esma_files(
                datasets=[file_type],
                date_from=date_from,
                date_to=date_to,
                file_type=file_type_filter,
                asset_type=asset_type,
            )

        if available:
            title = f"Available {file_type.upper()} Files (Last {days} days)"
            if dataset:
                title += f" - {dataset}"
            table = Table(title=title)
            table.add_column("Creation Date", style="green")
            table.add_column("Publication Date", style="blue")
            table.add_column("Filename", style="cyan")
            table.add_column("Size", style="yellow")
            table.add_column("Local Status", style="magenta")

            for file_info in available:
                # Check if file exists locally
                local_path = file_service.config.base_path / file_type / file_info.file_name
                is_local = (
                    local_path.exists() if hasattr(file_service.config, "base_path") else False
                )
                local_status = "Downloaded" if is_local else "Available"
                status_style = "green" if is_local else "yellow"

                # Format file size
                size_str = "N/A"
                if file_info.file_size:
                    if file_info.file_size > 1024 * 1024:
                        size_str = f"{file_info.file_size / (1024 * 1024):.1f} MB"
                    else:
                        size_str = f"{file_info.file_size / 1024:.1f} KB"

                table.add_row(
                    file_info.creation_date or "N/A",
                    file_info.publication_date or "N/A",
                    file_info.file_name or "N/A",
                    size_str,
                    f"[{status_style}]{local_status}[/{status_style}]",
                )
            console.print(table)

            # Summary
            total = len(available)
            console.print(f"[dim]Total available: {total} files[/dim]")
        else:
            console.print(
                f"[yellow]No {file_type.upper()} files available for the last {days} days[/yellow]"
            )

    except Exception as e:
        console.print(f"[red]Error checking available files: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# UTILITY COMMANDS
# ============================================================================


@cli.command()
@click.pass_context
def stats(ctx):
    """Show database statistics"""
    try:
        with console.status("[bold green]Gathering statistics..."):
            with get_session() as session:
                instrument_count = session.query(Instrument).count()
                transparency_count = session.query(TransparencyCalculation).count()
                mic_count = session.query(MarketIdentificationCode).count()
                legal_entity_count = session.query(LegalEntity).count()

                # Store counts for use outside session
                stats_data = {
                    "instruments": instrument_count,
                    "transparency": transparency_count,
                    "mics": mic_count,
                    "legal_entities": legal_entity_count,
                }

        stats_text = f"""[cyan]Instruments:[/cyan] {stats_data['instruments']:,}
[cyan]Transparency Calculations:[/cyan] {stats_data['transparency']:,}
[cyan]MIC Codes:[/cyan] {stats_data['mics']:,}
[cyan]Legal Entities:[/cyan] {stats_data['legal_entities']:,}"""

        console.print(Panel(stats_text, title="Database Statistics"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


@cli.command()
@click.argument("cfi_code")
@click.pass_context
def cfi(ctx, cfi_code):
    """Comprehensive CFI code analysis with all instrument levels"""
    try:
        from marketdata_api.models.utils.cfi_instrument_manager import (
            CFIInstrumentTypeManager,
            validate_cfi_code,
        )

        cfi_code = cfi_code.upper()

        with console.status(f"[bold green]Analyzing CFI code {cfi_code}..."):
            # Validate CFI code first
            is_valid, message = validate_cfi_code(cfi_code)

            if not is_valid:
                console.print(f"[red]Invalid CFI code: {message}[/red]")
                return

            # Get comprehensive CFI information using the improved structure
            cfi_info = CFIInstrumentTypeManager.get_cfi_info(cfi_code)

        if "error" in cfi_info:
            console.print(f"[red]Error analyzing CFI: {cfi_info['error']}[/red]")
            return

        # Create comprehensive details with all levels
        details = f"""[bold cyan]CFI Code:[/bold cyan] {cfi_info['cfi_code']}

[bold yellow]Classification Levels:[/bold yellow]
[cyan]Category:[/cyan] {cfi_info['category']} - {cfi_info['category_description']}
[cyan]Group:[/cyan] {cfi_info['group']} - {cfi_info['group_description']}
[cyan]Attributes:[/cyan] {cfi_info['attributes']}

[bold yellow]Business Information:[/bold yellow]
[cyan]Business Type:[/cyan] {cfi_info['business_type']}
[cyan]Is Equity:[/cyan] {'Yes' if cfi_info.get('is_equity') else 'No'}
[cyan]Is Debt:[/cyan] {'Yes' if cfi_info.get('is_debt') else 'No'}
[cyan]Is Collective Investment:[/cyan] {'Yes' if cfi_info.get('is_collective_investment') else 'No'}
[cyan]Is Derivative:[/cyan] {'Yes' if cfi_info.get('is_derivative') else 'No'}

[bold yellow]Technical Information:[/bold yellow]
[cyan]FITRS Patterns:[/cyan] {', '.join(cfi_info.get('fitrs_patterns', []))}"""

        # Add decoded attributes if available
        decoded_attrs = cfi_info.get("decoded_attributes", {})
        if decoded_attrs and isinstance(decoded_attrs, dict):
            details += "\n\n[bold yellow]Decoded Attributes:[/bold yellow]"
            for attr_name, attr_value in decoded_attrs.items():
                if attr_value and attr_value != "Unknown":
                    details += f"\n[cyan]{attr_name.replace('_', ' ').title()}:[/cyan] {attr_value}"

        console.print(Panel(details, title=f"Comprehensive CFI Analysis: {cfi_code}"))

        # Display additional classification flags in a table
        flags_table = Table(title="Classification Flags")
        flags_table.add_column("Type", style="cyan")
        flags_table.add_column("Status", style="green")

        flag_data = [
            ("Equity", "✓" if cfi_info.get("is_equity") else "✗"),
            ("Debt", "✓" if cfi_info.get("is_debt") else "✗"),
            ("Collective Investment", "✓" if cfi_info.get("is_collective_investment") else "✗"),
            ("Derivative", "✓" if cfi_info.get("is_derivative") else "✗"),
        ]

        for flag_type, status in flag_data:
            flags_table.add_row(flag_type, status)

        console.print(flags_table)

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


# ============================================================================
# DATABASE INITIALIZATION COMMAND
# ============================================================================


@cli.command()
@click.option(
    "--force", is_flag=True, help="Force recreate database (WARNING: destroys existing data)"
)
@click.option("--check-only", is_flag=True, help="Only check database status, do not initialize")
@click.pass_context
def init(ctx, force, check_only):
    """Initialize or check the MarketDataAPI database"""

    if check_only:
        console.print("[cyan]Checking database status...[/cyan]")
        if database_exists():
            console.print(f"[green]✓ Database exists:[/green] {SQLITE_DB_PATH}")
            # Try to verify tables
            from marketdata_api.database.initialize_db import verify_tables

            if verify_tables():
                console.print("[green]✓ Database structure is valid[/green]")
            else:
                console.print("[yellow]⚠️  Database structure may be incomplete[/yellow]")
        else:
            console.print(f"[red]✗ Database not found:[/red] {SQLITE_DB_PATH}")
            console.print("[dim]Run 'marketdata init' to create a new database[/dim]")
        return

    console.print("[cyan]MarketDataAPI Database Initialization[/cyan]\n")

    if database_exists() and not force:
        console.print(f"[yellow]Database already exists:[/yellow] {SQLITE_DB_PATH}")
        console.print("[dim]Use --force to recreate (WARNING: destroys existing data)[/dim]")
        console.print("[dim]Use --check-only to verify database structure[/dim]")
        return

    if force and database_exists():
        console.print(f"[red]⚠️  WARNING: About to recreate database at {SQLITE_DB_PATH}[/red]")
        console.print("[red]This will PERMANENTLY DELETE all existing data![/red]")

        if not click.confirm("Are you absolutely sure you want to continue?"):
            console.print("[yellow]Database initialization cancelled[/yellow]")
            return

    try:
        console.print("[cyan]Initializing database...[/cyan]")

        if init_database(force_recreate=force):
            console.print(f"[green]✓ Database initialized successfully![/green]")
            console.print(f"[dim]Location: {SQLITE_DB_PATH}[/dim]")
            console.print("\n[cyan]Next steps:[/cyan]")
            console.print("• Load MIC data: [yellow]marketdata mic remote update[/yellow]")
            console.print(
                "• Download FIRDS data: [yellow]marketdata files download firds --date 2025-09-20[/yellow]"
            )
            console.print("• Import instruments: [yellow]marketdata instruments import[/yellow]")
        else:
            console.print("[red]✗ Database initialization failed[/red]")
            console.print("[dim]Check the logs above for error details[/dim]")

    except Exception as e:
        console.print(f"[red]Database initialization failed: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback

            traceback.print_exc()


def main():
    """Entry point for the CLI when installed as a package"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        raise


if __name__ == "__main__":
    main()
