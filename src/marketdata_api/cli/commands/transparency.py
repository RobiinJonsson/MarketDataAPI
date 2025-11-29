"""
Transparency CLI commands for managing MiFID II transparency calculations.
"""
import click
from rich.panel import Panel
from rich.table import Table

from ..core.utils import console, handle_database_error


def _parse_raw_data(raw_data):
    """Parse raw_data field handling both dictionary (SQLite) and JSON string (SQL Server) formats."""
    if not raw_data:
        return {}
    
    if isinstance(raw_data, dict):
        return raw_data
    
    if isinstance(raw_data, str):
        try:
            import json
            return json.loads(raw_data)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    return {}


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
        from marketdata_api.config import DatabaseConfig
        
        # Dynamic model imports based on database type
        db_type = DatabaseConfig.get_database_type()
        if db_type == 'sqlite':
            from marketdata_api.models.sqlite.transparency import TransparencyCalculation
        else:
            from marketdata_api.models.sqlserver.transparency import SqlServerTransparencyCalculation as TransparencyCalculation
        
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
                # Add ORDER BY for SQL Server compatibility (MSSQL requires order_by when using OFFSET/LIMIT)
                for calc in query.order_by(TransparencyCalculation.id).limit(limit).offset(offset).all():
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
                    raw_data = _parse_raw_data(calc.raw_data)
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
        from marketdata_api.services.core.transparency_service import TransparencyService
        
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
@click.option("--full", is_flag=True, help="Show detailed analysis and comparisons")
@click.pass_context
@handle_database_error
def get_transparency(ctx, isin, full):
    """Get transparency calculations by ISIN with enhanced analysis"""
    try:
        from marketdata_api.services.core.transparency_service import TransparencyService
        from marketdata_api.services.core.instrument_service import InstrumentService
        
        service = TransparencyService()
        instrument_service = InstrumentService()

        with console.status(f"[bold green]Looking up transparency calculations for {isin}..."):
            calculations = service.get_transparency_by_isin(isin.upper())

        if not calculations:
            console.print(f"[red]❌ No transparency calculations found for ISIN: {isin}[/red]")
            return

        # Get instrument info for context
        instrument_session, instrument = instrument_service.get_instrument(isin.upper())
        
        # Display comprehensive transparency analysis
        _display_transparency_rich(calculations, instrument, full)
        
        if instrument_session:
            instrument_session.close()

    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


def _display_transparency_rich(calculations, instrument, show_full=False):
    """Display transparency calculations with rich formatting and analysis"""
    from rich.columns import Columns
    from rich.text import Text
    import datetime
    
    # Header with instrument context
    header_info = _format_transparency_header(calculations, instrument)
    console.print(Panel(header_info, title=f"📈 Transparency Analysis: {calculations[0].isin}", border_style="blue"))
    
    # Summary analysis
    summary_info = _format_transparency_summary(calculations)
    console.print(Panel(summary_info, title="📊 Summary Analysis", border_style="green"))
    
    if show_full:
        # Period comparison
        comparison_info = _format_period_comparison(calculations)
        if comparison_info.strip():
            console.print(Panel(comparison_info, title="📈 Period Comparison", border_style="yellow"))
        
        # Risk and liquidity analysis
        risk_info = _format_risk_analysis(calculations)
        if risk_info.strip():
            console.print(Panel(risk_info, title="⚠️ Risk & Liquidity Analysis", border_style="magenta"))
    
    # Individual calculation details
    console.print(f"\n[bold cyan]Individual Calculations ({len(calculations)} found):[/bold cyan]")
    for i, calculation in enumerate(calculations, 1):

        _display_calculation_details(calculation, i)


def _format_transparency_header(calculations, instrument):
    """Format header with instrument and transparency context"""
    if not calculations:
        return "No calculations available"
    
    calc = calculations[0]  # Use first calculation for context
    
    # Instrument context
    instrument_info = ""
    if instrument:
        instrument_info = f"""[bold white]{instrument.full_name or 'N/A'}[/bold white]
[dim]{instrument.instrument_type.title() if instrument.instrument_type else 'Unknown Type'} • {instrument.currency or 'N/A'}[/dim]

"""
    
    # Calculate date range across all calculations
    all_dates = []
    for calc in calculations:
        if calc.from_date:
            all_dates.append(calc.from_date)
        if calc.to_date:
            all_dates.append(calc.to_date)
    
    date_range = ""
    if all_dates:
        min_date = min(all_dates)
        max_date = max(all_dates)
        date_range = f"Data Period: {min_date.strftime('%Y-%m-%d') if hasattr(min_date, 'strftime') else min_date} to {max_date.strftime('%Y-%m-%d') if hasattr(max_date, 'strftime') else max_date}"
    
    return f"""{instrument_info}[cyan]ISIN:[/cyan] [bold]{calc.isin}[/bold]
[cyan]Calculations Found:[/cyan] {len(calculations)}
[cyan]{date_range}[/cyan]
[cyan]File Types:[/cyan] {', '.join(set(c.file_type for c in calculations if c.file_type))}"""


def _format_transparency_summary(calculations):
    """Format summary analysis of all calculations"""
    if not calculations:
        return "No data available"
    
    # Aggregate statistics
    total_volume = sum(c.total_volume_executed or 0 for c in calculations)
    total_transactions = sum(c.total_transactions_executed or 0 for c in calculations)
    
    # Find latest/most relevant calculation (with actual data)
    active_calcs = [c for c in calculations if c.total_transactions_executed and c.total_transactions_executed > 0]
    
    summary = []
    summary.append(f"[cyan]Total Volume (All Periods):[/cyan] {total_volume:,.2f}")
    summary.append(f"[cyan]Total Transactions:[/cyan] {total_transactions:,}")
    
    if active_calcs:
        avg_transaction_size = total_volume / total_transactions if total_transactions > 0 else 0
        summary.append(f"[cyan]Average Transaction Size:[/cyan] {avg_transaction_size:,.2f}")
        
        # Liquidity assessment
        liquid_count = sum(1 for c in calculations if c.liquidity is True)
        if liquid_count > 0:
            summary.append(f"[green]✅ Liquid Periods:[/green] {liquid_count}/{len(calculations)}")
        else:
            summary.append(f"[yellow]⚠️ Limited Liquidity Data Available[/yellow]")
    
    # Market activity insight
    if active_calcs:
        latest_active = max(active_calcs, key=lambda x: x.to_date or x.from_date or x.created_at)
        raw_data = _parse_raw_data(latest_active.raw_data)
        
        if raw_data.get('AvrgDalyTrnvr'):
            daily_turnover = float(raw_data['AvrgDalyTrnvr'])
            summary.append(f"[cyan]Latest Avg Daily Turnover:[/cyan] {daily_turnover:,.2f}")
        
        if raw_data.get('LrgInScale'):
            lis_threshold = float(raw_data['LrgInScale'])
            summary.append(f"[cyan]Large-in-Scale Threshold:[/cyan] {lis_threshold:,.0f}")
    
    return "\n".join(summary)


def _format_period_comparison(calculations):
    """Format comparison between different periods"""
    if len(calculations) < 2:
        return "Not enough periods for comparison"
    
    # Sort by period end date
    sorted_calcs = sorted(calculations, key=lambda x: x.to_date or x.from_date or x.created_at, reverse=True)
    
    comparison = []
    comparison.append("[bold]Period-over-Period Analysis:[/bold]")
    
    for i, calc in enumerate(sorted_calcs[:3]):  # Show top 3 periods
        period = f"{calc.from_date or 'N/A'} to {calc.to_date or 'N/A'}"
        volume = calc.total_volume_executed or 0
        transactions = calc.total_transactions_executed or 0
        
        volume_str = f"{volume:,.0f}" if volume > 0 else "No trading"
        tx_str = f"{transactions:,}" if transactions > 0 else "0"
        
        comparison.append(f"[cyan]Period {i+1}:[/cyan] {period}")
        comparison.append(f"  Volume: {volume_str} | Transactions: {tx_str}")
        
        # Calculate growth if possible
        if i < len(sorted_calcs) - 1:
            prev_calc = sorted_calcs[i + 1]
            prev_volume = prev_calc.total_volume_executed or 0
            
            if prev_volume > 0 and volume > 0:
                growth = ((volume - prev_volume) / prev_volume) * 100
                growth_color = "green" if growth > 0 else "red"
                comparison.append(f"  [{growth_color}]Volume Change: {growth:+.1f}%[/{growth_color}]")
    
    return "\n".join(comparison)


def _format_risk_analysis(calculations):
    """Format risk and liquidity analysis"""
    if not calculations:
        return "No data available"
    
    analysis = []
    analysis.append("[bold]Risk & Liquidity Assessment:[/bold]")
    
    # Find calculations with actual trading data
    active_calcs = [c for c in calculations if c.total_transactions_executed and c.total_transactions_executed > 0]
    
    if not active_calcs:
        analysis.append("[yellow]⚠️ No active trading periods found[/yellow]")
        return "\n".join(analysis)
    
    # Analyze trading patterns
    volumes = [c.total_volume_executed for c in active_calcs if c.total_volume_executed]
    if volumes and len(volumes) > 1:
        import statistics
        vol_std = statistics.stdev(volumes)
        vol_mean = statistics.mean(volumes)
        vol_cv = (vol_std / vol_mean) * 100 if vol_mean > 0 else 0
        
        analysis.append(f"[cyan]Volume Volatility (CV):[/cyan] {vol_cv:.1f}%")
        
        if vol_cv > 50:
            analysis.append("[red]🔴 High volume volatility - irregular trading[/red]")
        elif vol_cv > 25:
            analysis.append("[yellow]🟡 Moderate volume volatility[/yellow]")
        else:
            analysis.append("[green]🟢 Stable trading pattern[/green]")
    
    # Liquidity classification
    liquid_periods = sum(1 for c in calculations if c.liquidity is True)
    total_periods = len(calculations)
    
    if liquid_periods == 0:
        analysis.append("[red]🔴 No liquid periods identified[/red]")
    elif liquid_periods == total_periods:
        analysis.append("[green]🟢 Consistently liquid across all periods[/green]")
    else:
        liquidity_ratio = (liquid_periods / total_periods) * 100
        analysis.append(f"[yellow]🟡 Partially liquid: {liquidity_ratio:.0f}% of periods[/yellow]")
    
    return "\n".join(analysis)


def _display_calculation_details(calculation, index):
    """Display individual calculation details"""
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
[cyan]Period:[/cyan] {from_date} to {to_date}
[cyan]File Type:[/cyan] {calculation.file_type or 'N/A'}
[cyan]Liquidity:[/cyan] {'Yes' if calculation.liquidity else 'No' if calculation.liquidity is not None else 'Unknown'}
[cyan]Transactions:[/cyan] {transactions:,}
[cyan]Volume:[/cyan] {volume:,.2f}"""

    # Add asset-type-specific details from raw_data
    raw_data = _parse_raw_data(calculation.raw_data)

    # Check if this is equity data (FULECR files)
    is_equity = calculation.file_type and calculation.file_type.startswith("FULECR")

    if is_equity and raw_data:
        # Key equity metrics only
        details += f"""

[yellow]Key Metrics:[/yellow]
[cyan]Methodology:[/cyan] {raw_data.get('Mthdlgy', 'N/A')}
[cyan]Average Daily Turnover:[/cyan] {raw_data.get('AvrgDalyTrnvr', 'N/A')}
[cyan]Large in Scale Threshold:[/cyan] {raw_data.get('LrgInScale', 'N/A')}
[cyan]Standard Market Size:[/cyan] {raw_data.get('StdMktSz', 'N/A')}"""

    console.print(
        Panel(
            details, title=f"[bold]Calculation {index}[/bold]", border_style="cyan", padding=(0, 1)
        )
    )


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
        from marketdata_api.services.core.transparency_service import TransparencyService
        
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


@transparency.command()
@click.option("--isin", help="Check duplicates for specific ISIN (default: all ISINs)")
@click.option("--remove", is_flag=True, help="Remove duplicate records (keeps latest created)")
@click.option("--confirm", is_flag=True, help="Actually remove duplicates (required with --remove)")
@click.pass_context
@handle_database_error
def duplicates(ctx, isin, remove, confirm):
    """Detect and optionally remove duplicate transparency calculations."""
    from ...config import DatabaseConfig
    from ...database.session import get_session
    
    # Get database-agnostic imports
    db_type = DatabaseConfig.get_database_type()
    if db_type == "sqlite":
        from ...models.sqlite.transparency import SqliteTransparencyCalculation as TransparencyCalculation
    else:
        from ...models.sqlserver.transparency import SqlServerTransparencyCalculation as TransparencyCalculation
    
    with get_session() as session:
        # Build query to find duplicates
        query = session.query(TransparencyCalculation)
        if isin:
            query = query.filter(TransparencyCalculation.isin == isin)
        
        # Get all calculations ordered by ISIN, period, and created_at
        calculations = query.order_by(
            TransparencyCalculation.isin,
            TransparencyCalculation.from_date,
            TransparencyCalculation.to_date,
            TransparencyCalculation.file_type,
            TransparencyCalculation.created_at.desc()
        ).all()
        
        # Group by (isin, from_date, to_date, file_type) to find duplicates
        groups = {}
        for calc in calculations:
            key = (calc.isin, calc.from_date, calc.to_date, calc.file_type)
            if key not in groups:
                groups[key] = []
            groups[key].append(calc)
        
        # Find groups with duplicates
        duplicate_groups = {k: v for k, v in groups.items() if len(v) > 1}
        
        if not duplicate_groups:
            console.print("[green]No duplicate transparency calculations found.[/green]")
            return
        
        # Show duplicate summary
        total_duplicates = sum(len(group) - 1 for group in duplicate_groups.values())
        console.print(f"\n[yellow]Found {len(duplicate_groups)} groups with duplicates ({total_duplicates} excess records)[/yellow]")
        
        # Create table showing duplicates
        table = Table(title="Duplicate Transparency Calculations")
        table.add_column("ISIN", style="cyan")
        table.add_column("Period", style="blue")
        table.add_column("Type", style="magenta")
        table.add_column("Count", style="red")
        table.add_column("IDs (latest first)", style="dim")
        
        for (isin, from_date, to_date, file_type), calcs in duplicate_groups.items():
            period = f"{from_date} to {to_date}" if from_date and to_date else "N/A"
            ids_str = ", ".join(str(c.id)[:8] + "..." for c in calcs[:3])
            if len(calcs) > 3:
                ids_str += f" (+{len(calcs)-3} more)"
            
            table.add_row(
                isin or "N/A",
                period,
                file_type or "N/A", 
                str(len(calcs)),
                ids_str
            )
        
        console.print(table)
        
        if remove and confirm:
            # Remove duplicates (keep the latest created record for each group)
            removed_count = 0
            for calcs in duplicate_groups.values():
                # Keep the first (latest created), remove the rest
                for calc_to_remove in calcs[1:]:
                    session.delete(calc_to_remove)
                    removed_count += 1
            
            session.commit()
            console.print(f"\n[green]Removed {removed_count} duplicate records.[/green]")
            
        elif remove and not confirm:
            would_remove = sum(len(group) - 1 for group in duplicate_groups.values())
            console.print(f"\n[yellow]DRY RUN: Would remove {would_remove} duplicate records.[/yellow]")
            console.print("[dim]Use --remove --confirm to actually delete duplicates.[/dim]")
        
        else:
            # Just showing duplicates, no removal requested
            console.print(f"\n[dim]Use --remove --confirm to delete duplicate records.[/dim]")
        