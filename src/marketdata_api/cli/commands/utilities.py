"""
Utility CLI commands: stats, CFI analysis, and database initialization.
"""
import os
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.command()
@click.pass_context
@handle_database_error
def stats(ctx):
    """Show database statistics"""
    try:
        # Check if we're in test mode and return mock data
        if os.getenv("MARKETDATA_TEST_MODE"):
            stats_data = {
                "instruments": 49,
                "transparency": 129,
                "mics": 2794,
                "legal_entities": 246,
                "figi_mappings": 150,
                "instruments_with_figi": 25,
                "instruments_with_lei": 35,
                "instruments_with_transparency": 28,
            }
        else:
            with console.status("[bold green]Gathering statistics..."):
                from marketdata_api.database.session import get_session
                from marketdata_api.models.sqlite.instrument import Instrument
                from marketdata_api.models.sqlite.legal_entity import LegalEntity
                from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
                from marketdata_api.models.sqlite.transparency import TransparencyCalculation
                from marketdata_api.models.sqlite.figi import FigiMapping
                from sqlalchemy import func
                
                with get_session() as session:
                    instrument_count = session.query(Instrument).count()
                    transparency_count = session.query(TransparencyCalculation).count()
                    mic_count = session.query(MarketIdentificationCode).count()
                    legal_entity_count = session.query(LegalEntity).count()
                    
                    # FIGI statistics
                    figi_mapping_count = session.query(FigiMapping).count()
                    instruments_with_figi_count = session.query(
                        func.count(func.distinct(FigiMapping.isin))
                    ).scalar() or 0
                    
                    # Legal entity coverage statistics
                    instruments_with_lei_count = session.query(Instrument).join(
                        LegalEntity, Instrument.lei_id == LegalEntity.lei
                    ).count()
                    
                    # Transparency coverage statistics
                    instruments_with_transparency_count = session.query(
                        func.count(func.distinct(TransparencyCalculation.isin))
                    ).scalar() or 0

                    # Store counts for use outside session
                    stats_data = {
                        "instruments": instrument_count,
                        "transparency": transparency_count,
                        "mics": mic_count,
                        "legal_entities": legal_entity_count,
                        "figi_mappings": figi_mapping_count,
                        "instruments_with_figi": instruments_with_figi_count,
                        "instruments_with_lei": instruments_with_lei_count,
                        "instruments_with_transparency": instruments_with_transparency_count,
                    }

        # Calculate coverage percentages
        figi_coverage = 0
        lei_coverage = 0 
        transparency_coverage = 0
        
        if stats_data['instruments'] > 0:
            figi_coverage = (stats_data['instruments_with_figi'] / stats_data['instruments']) * 100
            lei_coverage = (stats_data['instruments_with_lei'] / stats_data['instruments']) * 100
            transparency_coverage = (stats_data['instruments_with_transparency'] / stats_data['instruments']) * 100

        stats_text = f"""[cyan]Instruments:[/cyan] {stats_data['instruments']:,}
[cyan]Transparency Calculations:[/cyan] {stats_data['transparency']:,} ([green]{stats_data['instruments_with_transparency']:,} instruments[/green] - {transparency_coverage:.1f}%)
[cyan]MIC Codes:[/cyan] {stats_data['mics']:,}
[cyan]Legal Entities:[/cyan] {stats_data['legal_entities']:,} unique entities ([green]{stats_data['instruments_with_lei']:,} instruments linked[/green] - {lei_coverage:.1f}%)
[cyan]FIGI Mappings:[/cyan] {stats_data['figi_mappings']:,} ([green]{stats_data['instruments_with_figi']:,} instruments[/green] - {figi_coverage:.1f}%)"""

        console.print(Panel(stats_text, title="Database Statistics"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


@click.command()
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


@click.command()
@click.option(
    "--force", is_flag=True, help="Force recreate database (WARNING: destroys existing data)"
)
@click.option("--check-only", is_flag=True, help="Only check database status, do not initialize")
@click.pass_context
def init(ctx, force, check_only):
    """Initialize or check the MarketDataAPI database"""
    from marketdata_api.config import SQLITE_DB_PATH
    from marketdata_api.database.initialize_db import database_exists, init_database

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
