"""
MIC CLI commands for Market Identification Code operations.
"""
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.group()
def mic():
    """Market Identification Code operations"""
    pass


@mic.command()
@click.option("--country", help="Filter by country code")
@click.option("--limit", default=20, help="Number of results")
@click.pass_context
@handle_database_error
def list(ctx, country, limit):
    """List MIC codes with optional filtering"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.market_identification_code import (
            MarketIdentificationCode,
            MICStatus,
        )
        
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
@handle_database_error
def get_mic(ctx, mic_code):
    """Get detailed MIC information"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
        
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
        from marketdata_api.services.mic_data_loader import remote_mic_service
        
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
