#!/usr/bin/env python3
"""
MarketDataAPI Professional CLI

A command-line interface for the MarketDataAPI using Click framework
for professional-grade CLI with proper command grouping, help, and error handling.

Install with: pip install -e .
Use with: marketdata instruments list
"""

import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Modern CLI framework
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# MarketDataAPI imports - moved to top level for efficiency
try:
    from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
    from marketdata_api.services.sqlite.legal_entity_service import LegalEntityService
    from marketdata_api.services.sqlite.transparency_service import TransparencyService
    from marketdata_api.services.mic_data_loader import MICDataLoader, remote_mic_service
    from marketdata_api.database.session import get_session
    from marketdata_api.models.sqlite.instrument import Instrument
    from marketdata_api.models.sqlite.transparency import TransparencyCalculation
    from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode, MICStatus
except ImportError as e:
    print(f"Error importing MarketDataAPI modules: {e}")
    print("Make sure you're in the correct project directory and the API is installed.")
    sys.exit(1)

# Initialize Rich console for beautiful output
console = Console()

# Custom Click group with better help formatting
class CustomGroup(click.Group):
    def format_help(self, ctx, formatter):
        """Custom help formatting with Rich styling"""
        console.print("\n[bold cyan]MarketDataAPI CLI[/bold cyan]")
        console.print("[dim]Professional command-line interface for financial market data[/dim]\n")
        super().format_help(ctx, formatter)

@click.group(cls=CustomGroup, invoke_without_command=True)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--format', type=click.Choice(['table', 'json', 'csv']), 
              default='table', help='Output format')
@click.pass_context
def cli(ctx, verbose, format):
    """MarketDataAPI CLI - Professional financial data interface"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['format'] = format
    
    if ctx.invoked_subcommand is None:
        console.print(Panel.fit(
            "[bold green]MarketDataAPI Professional CLI[/bold green]\n\n" +
            "[cyan]Available Commands:[/cyan]\n" +
            "• [yellow]instruments[/yellow] - Manage financial instruments\n" +
            "• [yellow]transparency[/yellow] - Transparency calculations\n" +
            "• [yellow]mic[/yellow] - Market identification codes\n" +
            "• [yellow]entities[/yellow] - Legal entities\n" +
            "• [yellow]stats[/yellow] - Database statistics\n" +
            "• [yellow]cfi[/yellow] - Comprehensive CFI code analysis\n\n" +
            "Use [green]--help[/green] with any command for details"
        ))

# ============================================================================
# INSTRUMENTS COMMAND GROUP
# ============================================================================

@cli.group()
def instruments():
    """Manage financial instruments (equities, bonds, derivatives, etc.)"""
    pass

@instruments.command()
@click.option('--type', help='Filter by instrument type')
@click.option('--currency', help='Filter by currency')
@click.option('--limit', default=20, help='Number of results to show')
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
                    instruments_data.append({
                        'isin': inst.isin,
                        'full_name': inst.full_name,
                        'instrument_type': inst.instrument_type,
                        'currency': inst.currency
                    })
        
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
                inst_data['isin'] or "N/A",
                (inst_data['full_name'] or "N/A")[:50] + ("..." if len(inst_data['full_name'] or "") > 50 else ""),
                inst_data['instrument_type'] or "N/A", 
                inst_data['currency'] or "N/A"
            )
        
        console.print(table)
        console.print(f"\n[dim]Showing {len(instruments_data)} instruments[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@instruments.command()
@click.argument('isin')
@click.pass_context  
def get(ctx, isin):
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
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@instruments.command()
@click.argument('isin')
@click.argument('instrument_type', default='equity')
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
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@instruments.command()
@click.argument('identifier')
@click.option('--type', default='equity', help='Instrument type for venue lookup')
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
                venue.get('venue_id', 'N/A'),
                venue.get('mic_code', 'N/A'),
                venue.get('first_trade_date', 'N/A'),
                venue.get('venue_status', 'N/A')
            )
            
        console.print(table)
        console.print(f"\n[dim]Found {len(venues_data)} venues[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
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
@click.option('--limit', default=20, help='Number of results')
@click.option('--offset', default=0, help='Results offset')
@click.pass_context
def list(ctx, limit, offset):
    """List transparency calculations"""
    try:
        with console.status("[bold green]Fetching transparency calculations..."):
            with get_session() as session:
                # Execute query and extract data within session context
                calculations_data = []
                for calc in session.query(TransparencyCalculation).limit(limit).offset(offset).all():
                    period = f"{calc.from_date} to {calc.to_date}" if calc.from_date and calc.to_date else "N/A"
                    liquidity = "✓" if calc.liquidity else "✗"
                    
                    calculations_data.append({
                        'id': str(calc.id)[:8] + "...",
                        'isin': calc.isin or "N/A",
                        'file_type': calc.file_type or "N/A",
                        'period': period,
                        'liquidity': liquidity
                    })
        
        if not calculations_data:
            console.print("[yellow]No transparency calculations found[/yellow]")
            return
            
        table = Table(title="Transparency Calculations")
        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("ISIN", style="green")
        table.add_column("File Type", style="magenta")
        table.add_column("Period", style="yellow")
        table.add_column("Liquid", style="red")
        
        for calc_data in calculations_data:
            table.add_row(
                calc_data['id'],
                calc_data['isin'],
                calc_data['file_type'],
                calc_data['period'],
                calc_data['liquidity']
            )
            
        console.print(table)
        console.print(f"\n[dim]Showing {len(calculations_data)} calculations (offset: {offset})[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@transparency.command()
@click.argument('transparency_id')
@click.pass_context
def get(ctx, transparency_id):
    """Get detailed transparency calculation by ID"""
    try:
        service = TransparencyService()
        
        with console.status(f"[bold green]Looking up transparency calculation..."):
            session, calculation = service.get_transparency_by_id(transparency_id)
        
        if not calculation:
            console.print(f"[red]Transparency calculation not found: {transparency_id}[/red]")
            return
            
        details = f"""[cyan]ID:[/cyan] {calculation.id}
[cyan]ISIN:[/cyan] {calculation.isin}
[cyan]File Type:[/cyan] {calculation.file_type}
[cyan]Period:[/cyan] {calculation.from_date} to {calculation.to_date}
[cyan]Liquidity:[/cyan] {'Yes' if calculation.liquidity else 'No'}
[cyan]Transactions:[/cyan] {calculation.total_transactions_executed:,}
[cyan]Volume:[/cyan] {calculation.total_volume_executed:,.2f if calculation.total_volume_executed else 'N/A'}
[cyan]Currency:[/cyan] {calculation.currency or 'N/A'}
[cyan]Venue:[/cyan] {calculation.trading_venue or 'N/A'}"""

        console.print(Panel(details, title="Transparency Calculation Details"))
        session.close()
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
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
@click.option('--country', help='Filter by country code')
@click.option('--limit', default=20, help='Number of results')
@click.pass_context
def list(ctx, country, limit):
    """List MIC codes with optional filtering"""
    try:
        with console.status("[bold green]Fetching MIC codes..."):
            with get_session() as session:
                query = session.query(MarketIdentificationCode).filter_by(
                    status=MICStatus.ACTIVE
                )
                if country:
                    query = query.filter_by(iso_country_code=country.upper())
                
                # Extract data within session context
                mics_data = []
                for mic in query.limit(limit).all():
                    mics_data.append({
                        'mic': mic.mic,
                        'market_name': mic.market_name,
                        'iso_country_code': mic.iso_country_code,
                        'city': mic.city
                    })
        
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
                mic_data['mic'],
                (mic_data['market_name'] or "N/A")[:40] + ("..." if len(mic_data['market_name'] or "") > 40 else ""),
                mic_data['iso_country_code'] or "N/A",
                mic_data['city'] or "N/A"
            )
            
        console.print(table)
        console.print(f"\n[dim]Showing {len(mics_data)} MIC codes[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@mic.command()
@click.argument('mic_code')
@click.pass_context
def get(ctx, mic_code):
    """Get detailed MIC information"""
    try:
        with console.status(f"[bold green]Looking up MIC {mic_code}..."):
            with get_session() as session:
                mic = session.query(MarketIdentificationCode).filter_by(mic=mic_code.upper()).first()
        
        if not mic:
            console.print(f"[red]MIC not found: {mic_code}[/red]")
            return
            
        details = f"""[cyan]MIC:[/cyan] {mic.mic}
[cyan]Market Name:[/cyan] {mic.market_name}
[cyan]Legal Entity:[/cyan] {mic.legal_entity_name or 'N/A'}
[cyan]Country:[/cyan] {mic.iso_country_code}
[cyan]City:[/cyan] {mic.city or 'N/A'}
[cyan]Status:[/cyan] {mic.status.value}
[cyan]Type:[/cyan] {mic.operation_type.value if mic.operation_type else 'N/A'}
[cyan]Operating MIC:[/cyan] {mic.operating_mic or 'N/A'}
[cyan]LEI:[/cyan] {mic.lei or 'N/A'}"""

        console.print(Panel(details, title=f"MIC Details: {mic_code.upper()}"))
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

# Remote MIC subcommand group
@mic.group()
def remote():
    """Real-time MIC operations using official ISO registry"""
    pass

@remote.command()
@click.argument('mic_code')
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
        if ctx.obj.get('verbose'):
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
@click.argument('lei')
@click.pass_context
def get(ctx, lei):
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
[cyan]Legal Form:[/cyan] {entity.legal_form or 'N/A'}
[cyan]Status:[/cyan] {entity.entity_status or 'N/A'}
[cyan]Jurisdiction:[/cyan] {entity.jurisdiction or 'N/A'}
[cyan]Created:[/cyan] {entity.created_at or 'N/A'}"""

        console.print(Panel(details, title=f"Legal Entity: {lei}"))
        session.close()
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
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
                
                # Store counts for use outside session
                stats_data = {
                    'instruments': instrument_count,
                    'transparency': transparency_count,
                    'mics': mic_count
                }
        
        stats_text = f"""[cyan]Instruments:[/cyan] {stats_data['instruments']:,}
[cyan]Transparency Calculations:[/cyan] {stats_data['transparency']:,}
[cyan]MIC Codes:[/cyan] {stats_data['mics']:,}"""

        console.print(Panel(stats_text, title="Database Statistics"))
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
            import traceback
            traceback.print_exc()

@cli.command()
@click.argument('cfi_code')
@click.pass_context
def cfi(ctx, cfi_code):
    """Comprehensive CFI code analysis with all instrument levels"""
    try:
        from marketdata_api.models.utils.cfi_instrument_manager import CFIInstrumentTypeManager, validate_cfi_code
        
        cfi_code = cfi_code.upper()
        
        with console.status(f"[bold green]Analyzing CFI code {cfi_code}..."):
            # Validate CFI code first
            is_valid, message = validate_cfi_code(cfi_code)
            
            if not is_valid:
                console.print(f"[red]Invalid CFI code: {message}[/red]")
                return
                
            # Get comprehensive CFI information using the improved structure
            cfi_info = CFIInstrumentTypeManager.get_cfi_info(cfi_code)
        
        if 'error' in cfi_info:
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
        decoded_attrs = cfi_info.get('decoded_attributes', {})
        if decoded_attrs and isinstance(decoded_attrs, dict):
            details += "\n\n[bold yellow]Decoded Attributes:[/bold yellow]"
            for attr_name, attr_value in decoded_attrs.items():
                if attr_value and attr_value != 'Unknown':
                    details += f"\n[cyan]{attr_name.replace('_', ' ').title()}:[/cyan] {attr_value}"

        console.print(Panel(details, title=f"Comprehensive CFI Analysis: {cfi_code}"))
        
        # Display additional classification flags in a table
        flags_table = Table(title="Classification Flags")
        flags_table.add_column("Type", style="cyan")
        flags_table.add_column("Status", style="green")
        
        flag_data = [
            ("Equity", "✓" if cfi_info.get('is_equity') else "✗"),
            ("Debt", "✓" if cfi_info.get('is_debt') else "✗"),
            ("Collective Investment", "✓" if cfi_info.get('is_collective_investment') else "✗"),
            ("Derivative", "✓" if cfi_info.get('is_derivative') else "✗")
        ]
        
        for flag_type, status in flag_data:
            flags_table.add_row(flag_type, status)
            
        console.print(flags_table)
        
    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get('verbose'):
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

if __name__ == '__main__':
    main()
