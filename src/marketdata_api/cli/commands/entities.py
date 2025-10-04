"""
Entities CLI commands for legal entity management.
"""
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.group()
def entities():
    """Legal entity operations"""
    pass


@entities.command()
@click.option("--country", help="Filter by country code")
@click.option("--limit", default=20, help="Number of results")
@click.pass_context
@handle_database_error
def list(ctx, country, limit):
    """List legal entities with optional filtering"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.legal_entity import LegalEntity
        
        with console.status("[bold green]Fetching legal entities..."):
            with get_session() as session:
                query = session.query(LegalEntity)
                if country:
                    query = query.filter_by(country=country.upper())

                # Extract data within session context
                entities_data = []
                for entity in query.limit(limit).all():
                    entities_data.append(
                        {
                            "lei": entity.lei,
                            "legal_name": entity.legal_name,
                            "country": entity.country,
                            "status": entity.status,
                        }
                    )

        if not entities_data:
            console.print("[yellow]No legal entities found[/yellow]")
            return

        table = Table(title=f"Legal Entities{f' for {country.upper()}' if country else ''}")
        table.add_column("LEI", style="cyan", no_wrap=True)
        table.add_column("Legal Name", style="green")
        table.add_column("Country", style="magenta")
        table.add_column("Status", style="yellow")

        for entity_data in entities_data:
            table.add_row(
                entity_data["lei"],
                (entity_data["legal_name"] or "N/A")[:50]
                + ("..." if len(entity_data["legal_name"] or "") > 50 else ""),
                entity_data["country"] or "N/A",
                entity_data["status"] or "N/A",
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
@handle_database_error
def get_entity(ctx, lei):
    """Get detailed legal entity information"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.legal_entity import LegalEntity
        
        with console.status(f"[bold green]Looking up LEI {lei}..."):
            with get_session() as session:
                entity = session.query(LegalEntity).filter_by(lei=lei).first()

                if not entity:
                    console.print(f"[red]Legal entity not found: {lei}[/red]")
                    return

                # Extract all data while session is active
                entity_data = {
                    "lei": entity.lei,
                    "legal_name": entity.legal_name,
                    "country": entity.country,
                    "status": entity.status,
                    "legal_form": entity.legal_form,
                    "address": entity.address,
                    "city": entity.city,
                    "postal_code": entity.postal_code,
                }

        details = f"""[cyan]LEI:[/cyan] {entity_data['lei']}
[cyan]Legal Name:[/cyan] {entity_data['legal_name']}
[cyan]Country:[/cyan] {entity_data['country']}
[cyan]Status:[/cyan] {entity_data['status'] or 'N/A'}
[cyan]Legal Form:[/cyan] {entity_data['legal_form'] or 'N/A'}
[cyan]Address:[/cyan] {entity_data['address'] or 'N/A'}
[cyan]City:[/cyan] {entity_data['city'] or 'N/A'}
[cyan]Postal Code:[/cyan] {entity_data['postal_code'] or 'N/A'}"""

        console.print(Panel(details, title=f"Legal Entity Details: {lei}"))

    except Exception as e:
        console.print(f"[red]Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()
