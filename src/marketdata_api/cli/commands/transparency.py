"""
Transparency CLI commands for managing MiFID II transparency calculations.
"""
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


@click.group()
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
@handle_database_error
def list(ctx, limit, offset, type, liquidity, threshold, isin):
    """List transparency calculations with advanced filtering"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.transparency import TransparencyCalculation
        
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
                    volume_formatted = "N/A"
                    if calc.total_volume_executed is not None:
                        if calc.total_volume_executed >= 1_000_000:
                            volume_formatted = f"{calc.total_volume_executed/1_000_000:.1f}M"
                        elif calc.total_volume_executed >= 1_000:
                            volume_formatted = f"{calc.total_volume_executed/1_000:.1f}K"
                        else:
                            volume_formatted = f"{calc.total_volume_executed:.0f}"

                    # Format transactions
                    transactions_formatted = "N/A"
                    if calc.total_transactions_executed is not None:
                        if calc.total_transactions_executed >= 1_000_000:
                            transactions_formatted = f"{calc.total_transactions_executed/1_000_000:.1f}M"
                        elif calc.total_transactions_executed >= 1_000:
                            transactions_formatted = f"{calc.total_transactions_executed/1_000:.1f}K"
                        else:
                            transactions_formatted = f"{calc.total_transactions_executed:,}"

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
                            "volume": volume_formatted,
                            "transactions": transactions_formatted,
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
@handle_database_error
def create(ctx, isin, type):
    """Create transparency calculations for an ISIN from FITRS data"""
    try:
        from marketdata_api.services.sqlite.transparency_service import TransparencyService
        
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
@handle_database_error
def get_transparency(ctx, isin):
    """Get transparency calculations by ISIN"""
    try:
        from marketdata_api.services.sqlite.transparency_service import TransparencyService
        
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

[yellow]Equity-Specific Data:[/yellow]
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

[yellow]Non-Equity Data:[/yellow]
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
@handle_database_error
def bulk_create(ctx, limit, batch_size, skip_existing):
    """Create transparency calculations in bulk for instruments without them"""
    try:
        from marketdata_api.services.sqlite.transparency_service import TransparencyService
        
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