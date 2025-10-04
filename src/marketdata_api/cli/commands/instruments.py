"""
Instruments CLI commands for managing financial instruments.
"""
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.group()
def instruments():
    """Manage financial instruments (equities, bonds, derivatives, etc.)"""
    pass


@instruments.command()
@click.option("--type", help="Filter by instrument type")
@click.option("--currency", help="Filter by currency")
@click.option("--limit", default=20, help="Number of results to show")
@click.pass_context
@handle_database_error
def list(ctx, type, currency, limit):
    """List instruments with optional filtering"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.instrument import Instrument
        
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
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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
@handle_database_error
def create(ctx, isin, instrument_type):
    """Create instrument from external data sources (FIRDS)"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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
@handle_database_error
def enrich(ctx, isin):
    """Enrich existing instrument with external data (FIGI, LEI, etc.)"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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
                figi_count = len(enriched_instrument.figi_mappings)
                enrichment_info.append(f"[green]{figi_count} FIGI mapping(s)[/green]")
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
@handle_database_error
def bulk_create(ctx, jurisdiction, type, limit, batch_size, skip_existing, enrichment):
    """Create multiple instruments in bulk with filtering"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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
@handle_database_error
def venues(ctx, identifier, type):
    """Get trading venues for an instrument"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
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