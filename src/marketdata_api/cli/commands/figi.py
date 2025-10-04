"""
FIGI CLI commands for Financial Instrument Global Identifier operations.
"""
import click
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.group()
def figi():
    """FIGI (Financial Instrument Global Identifier) operations"""
    pass


@figi.command("get")
@click.argument("isin")
@click.pass_context
@handle_database_error
def get_figi(ctx, isin):
    """Get FIGI mappings for an ISIN"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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
