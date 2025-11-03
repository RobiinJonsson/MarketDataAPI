"""
Instruments CLI commands for managing financial instruments.
"""
import click
from datetime import datetime
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
@click.option("--full", is_flag=True, help="Show complete details including relationships")
@click.option("--format", type=click.Choice(['rich', 'json', 'table']), default='rich', help="Output format")
@click.pass_context
@handle_database_error
def get_instrument(ctx, isin, full, format):
    """Get detailed instrument information by ISIN with rich formatting"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        import json
        from rich.columns import Columns
        from rich.text import Text
        
        service = SqliteInstrumentService()

        with console.status(f"[bold green]Looking up {isin}..."):
            session, instrument = service.get_instrument(isin)

        if not instrument:
            console.print(f"[red]❌ Instrument not found: {isin}[/red]")
            return

        if format == 'json':
            # JSON output for programmatic use
            api_response = instrument.to_api_response()
            console.print(json.dumps(api_response, indent=2, default=str))
            session.close()
            return

        # Rich formatted output
        _display_instrument_rich(instrument, full)
        session.close()

    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
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
@click.argument("isin")
@click.option("--cascade", is_flag=True, help="Delete related data (venues, FIGI mappings, etc.)")
@click.option("--force", is_flag=True, help="Skip confirmation prompt")
@click.pass_context
@handle_database_error
def delete(ctx, isin, cascade, force):
    """Delete an instrument and optionally its related data"""
    try:
        from marketdata_api.services.sqlite.instrument_service import SqliteInstrumentService
        
        service = SqliteInstrumentService()

        # First verify the instrument exists
        with console.status(f"[bold green]Looking up instrument {isin}..."):
            session, instrument = service.get_instrument(isin)

        if not instrument:
            console.print(f"[red]❌ Instrument not found: {isin}[/red]")
            return

        # Show what will be deleted
        console.print(f"[yellow]⚠️  About to delete instrument:[/yellow]")
        console.print(f"  ISIN: [bold]{instrument.isin}[/bold]")
        console.print(f"  Name: {instrument.full_name or 'N/A'}")
        console.print(f"  Type: {instrument.instrument_type}")
        
        # Show related data that exists
        related_data = []
        if hasattr(instrument, 'trading_venues') and instrument.trading_venues:
            related_data.append(f"{len(instrument.trading_venues)} trading venue(s)")
        if hasattr(instrument, 'figi_mappings') and instrument.figi_mappings:
            related_data.append(f"{len(instrument.figi_mappings)} FIGI mapping(s)")
        if hasattr(instrument, 'legal_entity') and instrument.legal_entity:
            related_data.append("legal entity data")
        if hasattr(instrument, 'transparency_calculations') and instrument.transparency_calculations:
            related_data.append(f"{len(instrument.transparency_calculations)} transparency calculation(s)")
        
        if related_data:
            console.print(f"  Related data: {', '.join(related_data)}")
            if cascade:
                console.print("[red]  → Related data will also be deleted (--cascade)[/red]")
            else:
                console.print("[yellow]  → Related data will be preserved (use --cascade to delete)[/yellow]")
        
        session.close()

        # Confirmation prompt
        if not force:
            import click
            if not click.confirm(f"\n[red]Are you sure you want to delete {isin}?[/red]", abort=True):
                console.print("[yellow]Deletion cancelled[/yellow]")
                return

        # Perform deletion
        with console.status(f"[bold red]Deleting instrument {isin}..."):
            success = service.delete_instrument(isin, cascade=cascade)

        if success:
            console.print(f"[green]✓[/green] Successfully deleted instrument: {isin}")
            if cascade:
                console.print("  [green]✓[/green] Related data also removed")
        else:
            console.print(f"[red]❌ Failed to delete instrument: {isin}[/red]")

    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
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
                competent_authority=jurisdiction,
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


def _display_instrument_rich(instrument, show_full=False):
    """Display instrument with rich formatting and comprehensive details"""
    from rich.columns import Columns
    from rich.text import Text
    
    # Main instrument panel
    main_details = _format_main_instrument_panel(instrument)
    console.print(Panel(main_details, title=f"📊 {instrument.isin}", border_style="blue"))
    
    # Financial Details Panel  
    financial_details = _format_financial_details_panel(instrument)
    if financial_details.strip():
        console.print(Panel(financial_details, title="💰 Financial Details", border_style="green"))
    
    # Type-specific attributes
    type_attrs = _format_type_specific_attributes(instrument)
    if type_attrs.strip():
        console.print(Panel(type_attrs, title=f"🏷️ {instrument.instrument_type.title()} Attributes", border_style="yellow"))
    
    if show_full:
        # Legal Entity Information
        if instrument.legal_entity:
            entity_details = _format_legal_entity_panel(instrument.legal_entity)
            console.print(Panel(entity_details, title="🏢 Issuer Information", border_style="magenta"))
        
        # Trading Venues
        if instrument.trading_venues:
            venues_table = _format_trading_venues_table(instrument.trading_venues)
            console.print(Panel(venues_table, title="🏛️ Trading Venues", border_style="cyan"))
        
        # FIGI Mappings
        if instrument.figi_mappings:
            figi_details = _format_figi_mappings(instrument.figi_mappings)
            console.print(Panel(figi_details, title="🔗 FIGI Mappings", border_style="bright_blue"))
        
        # Transparency Calculations
        if instrument.transparency_calculations:
            transparency_details = _format_transparency_data(instrument.transparency_calculations)
            console.print(Panel(transparency_details, title="📈 Transparency Data", border_style="bright_green"))


def _format_main_instrument_panel(instrument):
    """Format the main instrument identification panel"""
    # CFI Code with description
    cfi_desc = _get_cfi_description(instrument.cfi_code) if instrument.cfi_code else "N/A"
    cfi_display = f"{instrument.cfi_code or 'N/A'}" + (f" ({cfi_desc})" if cfi_desc != "N/A" else "")
    
    # Status indicators
    status_icons = []
    if instrument.commodity_derivative_indicator:
        status_icons.append("🌾 Commodity Derivative")
    if instrument.legal_entity:
        status_icons.append("✅ Issuer Verified")
    if instrument.figi_mappings:
        status_icons.append("🏷️ FIGI Mapped")
    
    status_line = " • ".join(status_icons) if status_icons else "ℹ️ Basic Information"
    
    return f"""[bold white]{instrument.full_name or 'N/A'}[/bold white]
[dim]{instrument.short_name or 'No short name available'}[/dim]

[cyan]ISIN:[/cyan] [bold]{instrument.isin}[/bold]
[cyan]Type:[/cyan] [bold green]{instrument.instrument_type.title()}[/bold green]
[cyan]CFI Code:[/cyan] {cfi_display}
[cyan]Currency:[/cyan] [bold]{instrument.currency or 'N/A'}[/bold]
[cyan]LEI ID:[/cyan] {instrument.lei_id or 'N/A'}

[dim]{status_line}[/dim]"""


def _format_financial_details_panel(instrument):
    """Format financial and regulatory details"""
    details = []
    
    if instrument.competent_authority:
        details.append(f"[cyan]Regulator:[/cyan] {instrument.competent_authority}")
    
    # Enhanced primary venue display with MIC lookup
    if instrument.relevant_trading_venue:
        primary_venue_display = _format_primary_venue_with_mic(instrument.relevant_trading_venue)
        details.append(f"[cyan]Primary Venue:[/cyan] {primary_venue_display}")
    
    if instrument.publication_from_date:
        date_str = instrument.publication_from_date.strftime("%Y-%m-%d") if isinstance(instrument.publication_from_date, datetime) else str(instrument.publication_from_date)
        details.append(f"[cyan]Published:[/cyan] {date_str}")
    
    # Extract financial data from FIRDS fields
    if instrument.firds_data and isinstance(instrument.firds_data, dict):
        firds = instrument.firds_data
        
        # Price multiplier (common across derivatives)
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            details.append(f"[cyan]Price Multiplier:[/cyan] {firds['DerivInstrmAttrbts_PricMltplr']}")
            
        # Debt-specific financial fields
        if firds.get('DebtInstrmAttrbts_TtlIssdNmnlAmt'):
            amount = firds['DebtInstrmAttrbts_TtlIssdNmnlAmt']
            details.append(f"[cyan]Total Issued:[/cyan] {int(amount):,} {instrument.currency or ''}")
            
        if firds.get('DebtInstrmAttrbts_NmnlValPerUnit'):
            nominal = firds['DebtInstrmAttrbts_NmnlValPerUnit']
            details.append(f"[cyan]Nominal per Unit:[/cyan] {nominal}")
            
        if firds.get('DebtInstrmAttrbts_IntrstRate_Fxd'):
            rate = firds['DebtInstrmAttrbts_IntrstRate_Fxd']
            details.append(f"[cyan]Fixed Interest Rate:[/cyan] {rate}%")
    
    return "\n".join(details)


def _format_primary_venue_with_mic(mic_code):
    """Format primary venue with rich MIC data lookup"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
        
        with get_session() as session:
            mic_data = session.query(MarketIdentificationCode).filter(
                MarketIdentificationCode.mic == mic_code
            ).first()
            
            if mic_data:
                # Build rich display with MIC information
                venue_display = f"{mic_code}"
                if mic_data.market_name:
                    # Truncate long market names
                    market_name = mic_data.market_name
                    if len(market_name) > 40:
                        market_name = market_name[:37] + "..."
                    venue_display += f" ({market_name})"
                
                if mic_data.iso_country_code:
                    venue_display += f" [{mic_data.iso_country_code}]"
                    
                # Add status indicator
                if mic_data.status and mic_data.status.value == "ACTIVE":
                    venue_display += " [green]●[/green]"
                elif mic_data.status and mic_data.status.value in ["EXPIRED", "SUSPENDED"]:
                    venue_display += " [red]●[/red]"
                    
                return venue_display
            else:
                return f"{mic_code} (MIC not found in registry)"
                
    except Exception:
        # Fallback to basic display if lookup fails
        return mic_code


def _get_commodity_classification(firds_data):
    """Extract and format commodity classification information from FIRDS data"""
    classification_info = {
        'icon': '🌾',
        'display_name': 'Commodity',
        'additional_info': ''
    }
    
    # Natural Gas futures
    if (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_BasePdct') or
        firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_SubPdct')):
        classification_info.update({
            'icon': '⛽',
            'display_name': 'Natural Gas',
            'additional_info': firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_NtrlGas_AddtlSubPdct', '')
        })
    
    # Agricultural - Seafood
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Sfd_SubPdct')):
        classification_info.update({
            'icon': '🐟',
            'display_name': 'Seafood',
            'additional_info': 'Agricultural derivative'
        })
    
    # Agricultural - Dairy
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Dairy_SubPdct')):
        classification_info.update({
            'icon': '🥛',
            'display_name': 'Dairy Products',
            'additional_info': 'Agricultural derivative'
        })
    
    # Agricultural - Grains
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_Grn_SubPdct')):
        classification_info.update({
            'icon': '🌾',
            'display_name': 'Grains',
            'additional_info': 'Agricultural derivative'
        })
    
    # Agricultural - Oil Seeds
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrnOilSeed_SubPdct')):
        classification_info.update({
            'icon': '🌻',
            'display_name': 'Oil Seeds',
            'additional_info': 'Agricultural derivative'
        })
    
    # Energy - Electricity
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Elctrcty_SubPdct')):
        classification_info.update({
            'icon': '⚡',
            'display_name': 'Electricity',
            'additional_info': 'Energy derivative'
        })
    
    # Environmental - Emissions
    elif (firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_BasePdct') or
          firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Envttl_Emssns_SubPdct')):
        classification_info.update({
            'icon': '🌍',
            'display_name': 'Carbon Emissions',
            'additional_info': 'Environmental derivative'
        })
    
    # Only return if we found actual commodity classification
    base_product_found = any([
        firds_data.get(key) for key in firds_data.keys() 
        if '_BasePdct' in key and firds_data.get(key)
    ])
    
    return classification_info if base_product_found else None


def _get_swap_classification(instrument, firds_data):
    """Extract and format swap classification information from CFI code and FIRDS data"""
    try:
        cfi_code = instrument.cfi_code
        
        if not cfi_code or len(cfi_code) < 6:
            return None
        
        classification_info = {
            'icon': '🔄',
            'display_name': 'Swap',
            'additional_info': '',
            'swap_details': {}
        }
    except Exception as e:
        # Return basic info if there's an error
        return {
            'icon': '🔄',
            'display_name': 'Swap',
            'additional_info': f'Error in classification: {str(e)}',
            'swap_details': {}
        }
    
    # Credit Default Swaps (SCBCCA)
    if cfi_code == 'SCBCCA':
        classification_info.update({
            'icon': '💳',
            'display_name': 'Credit Default Swap',
            'additional_info': 'Credit protection derivative'
        })
        
        # Extract basket information
        if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
            basket_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
            classification_info['swap_details']['basket_isin'] = basket_isin
    
    # Equity Total Return Swaps (SESTXC)  
    elif cfi_code == 'SESTXC':
        classification_info.update({
            'icon': '📈',
            'display_name': 'Equity Total Return Swap',
            'additional_info': 'Equity exposure derivative'
        })
        
        # Extract underlying equity information
        if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            underlying_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
            classification_info['swap_details']['underlying_isin'] = underlying_isin
    
    # Foreign Exchange Swaps (SFCXXP)
    elif cfi_code == 'SFCXXP':
        classification_info.update({
            'icon': '💱',
            'display_name': 'Foreign Exchange Swap',
            'additional_info': 'Currency exchange derivative'
        })
        
        # Extract FX pair information
        base_currency = instrument.currency
        other_currency = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy')
        if base_currency and other_currency:
            classification_info['swap_details']['currency_pair'] = f"{base_currency}/{other_currency}"
    
    # Interest Rate Swaps - Standard (SRCCSP)
    elif cfi_code == 'SRCCSP':
        classification_info.update({
            'icon': '📊',
            'display_name': 'Interest Rate Swap',
            'additional_info': 'Fixed-float interest rate derivative'
        })
        
        # Extract interest rate information
        ref_rate = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm')
        if ref_rate:
            classification_info['swap_details']['reference_rate'] = ref_rate
        
        term_val = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val')
        term_unit = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit')
        if term_val and term_unit:
            if term_unit == 'MNTH':
                term_display = f"{term_val} Month{'s' if int(term_val) != 1 else ''}"
            elif term_unit == 'YEAR':
                term_display = f"{term_val} Year{'s' if int(term_val) != 1 else ''}"
            else:
                term_display = f"{term_val} {term_unit}"
            classification_info['swap_details']['floating_term'] = term_display
    
    # Interest Rate Swaps - OIS (SRHCSC)  
    elif cfi_code == 'SRHCSC':
        classification_info.update({
            'icon': '🏦',
            'display_name': 'OIS Interest Rate Swap',
            'additional_info': 'Overnight indexed swap'
        })
        
        # Extract OIS-specific information
        ref_rate = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Nm')
        if ref_rate:
            classification_info['swap_details']['ois_rate'] = ref_rate
        
        term_val = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val')
        term_unit = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit')
        if term_val and term_unit:
            if term_unit == 'DAYS':
                term_display = f"{term_val} Day{'s' if int(term_val) != 1 else ''}"
            elif term_unit == 'YEAR':
                term_display = f"{term_val} Year{'s' if int(term_val) != 1 else ''}"
            else:
                term_display = f"{term_val} {term_unit}"
            classification_info['swap_details']['compound_period'] = term_display
    
    return classification_info


def _get_forward_classification(instrument, firds_data):
    """Extract and format forward classification information from CFI code and FIRDS data"""
    try:
        cfi_code = instrument.cfi_code
        
        if not cfi_code or len(cfi_code) < 6:
            return None
        
        classification_info = {
            'icon': '⏩',
            'display_name': 'Forward',
            'additional_info': '',
            'forward_details': {}
        }
    except Exception as e:
        # Return basic info if there's an error
        return {
            'icon': '⏩',
            'display_name': 'Forward',
            'additional_info': f'Error in classification: {str(e)}',
            'forward_details': {}
        }
    
    # Analyze CFI structure: JEBXFC, JFTXFC, JRMXFP, JRMXSC
    if len(cfi_code) >= 2:
        second_char = cfi_code[1]
        
        # Equity Forwards (JE****) 
        if second_char == 'E':
            classification_info.update({
                'icon': '📈',
                'display_name': 'Equity Forward',
                'additional_info': 'Forward contract on equity underlying'
            })
            
            # Extract underlying basket information
            if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
                basket_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
                classification_info['forward_details']['basket_isin'] = basket_isin
                classification_info['additional_info'] += ' (basket)'
        
        # Foreign Exchange Forwards (JF****)
        elif second_char == 'F':
            classification_info.update({
                'icon': '💱',
                'display_name': 'FX Forward',
                'additional_info': 'Foreign exchange forward contract'
            })
            
            # Extract FX type and currency pair
            fx_type = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp')
            other_currency = firds_data.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy')
            
            if fx_type:
                if fx_type == 'FXCR':
                    classification_info['additional_info'] = 'Non-Deliverable Forward (NDF)'
                elif fx_type == 'FXSW':
                    classification_info['additional_info'] = 'FX swap forward leg'
                else:
                    classification_info['forward_details']['fx_type'] = fx_type
            
            if other_currency and instrument.currency:
                classification_info['forward_details']['currency_pair'] = f"{instrument.currency}/{other_currency}"
        
        # Rate Forwards (JR****)
        elif second_char == 'R':
            classification_info.update({
                'icon': '📊',
                'display_name': 'Rate Forward',
                'additional_info': 'Interest rate forward contract'
            })
            
            # Determine specific rate forward type from CFI position 3
            if len(cfi_code) >= 3:
                third_char = cfi_code[2]
                if third_char == 'M':  # JRMXFP, JRMXSC pattern
                    classification_info['display_name'] = 'Rate Forward (FRA)'
                    classification_info['additional_info'] = 'Forward Rate Agreement'
            
            # Extract underlying instrument
            underlying_isin = firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN')
            if underlying_isin:
                classification_info['forward_details']['underlying_isin'] = underlying_isin
            
            # Extract term information
            term_val = firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val')
            term_unit = firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit')
            if term_val and term_unit:
                if term_unit == 'WEEK':
                    term_display = f"{term_val} Week{'s' if int(term_val) != 1 else ''}"
                elif term_unit == 'YEAR':
                    term_display = f"{term_val} Year{'s' if int(term_val) != 1 else ''}"
                else:
                    term_display = f"{term_val} {term_unit}"
                classification_info['forward_details']['forward_term'] = term_display
        
        # Commodity Forwards (JC****)
        elif second_char == 'C':
            classification_info.update({
                'icon': '🌾',
                'display_name': 'Commodity Forward',
                'additional_info': 'Forward contract on commodity underlying'
            })
    
    return classification_info


def _get_structured_classification(instrument, firds_data):
    """Extract and format structured product classification information from CFI code and FIRDS data"""
    try:
        cfi_code = instrument.cfi_code
        
        if not cfi_code or len(cfi_code) < 6:
            return None
        
        classification_info = {
            'icon': '🏗️',
            'display_name': 'Structured Product',
            'additional_info': '',
            'structured_details': {}
        }
    except Exception as e:
        # Return basic info if there's an error
        return {
            'icon': '🏗️',
            'display_name': 'Structured Product',
            'additional_info': f'Error in classification: {str(e)}',
            'structured_details': {}
        }
    
    # Analyze CFI structure for H-category instruments
    if len(cfi_code) >= 2:
        second_char = cfi_code[1]  # Group character
        
        # Certificates and Capital Protection (HC****)
        if second_char == 'C':
            classification_info.update({
                'icon': '🏛️',
                'display_name': 'Capital Protection Certificate',
                'additional_info': 'Structured product with capital protection features'
            })
            
            # Extract certificate type from CFI 3rd character
            if len(cfi_code) >= 3:
                cert_type = cfi_code[2]
                if cert_type == 'A':
                    classification_info['display_name'] = 'Tracker Certificate'
                    classification_info['additional_info'] = '1:1 participation in underlying performance'
                elif cert_type == 'B':
                    classification_info['display_name'] = 'Outperformance Certificate'
                    classification_info['additional_info'] = 'Leveraged participation above strike level'
                elif cert_type == 'C':
                    classification_info['display_name'] = 'Bonus Certificate'
                    classification_info['additional_info'] = 'Minimum redemption with barrier protection'
                elif cert_type == 'D':
                    classification_info['display_name'] = 'Outperformance Bonus Certificate'
                    classification_info['additional_info'] = 'Leveraged upside with barrier protection'
                elif cert_type == 'E':
                    classification_info['display_name'] = 'Twin-Win Certificate'
                    classification_info['additional_info'] = 'Profits from both rising and falling markets'
        
        # Partial Protection (HP****)
        elif second_char == 'P':
            classification_info.update({
                'icon': '🛡️',
                'display_name': 'Partial Protection Product',
                'additional_info': 'Limited downside protection with upside participation'
            })
        
        # Yield Enhancement (HY****)
        elif second_char == 'Y':
            classification_info.update({
                'icon': '💰',
                'display_name': 'Yield Enhancement Product',
                'additional_info': 'Income-focused structured product'
            })
            
            # Common yield enhancement types
            if firds_data.get('DerivInstrmAttrbts_OptnTp'):
                option_type = firds_data['DerivInstrmAttrbts_OptnTp']
                if option_type in ['CALL', 'PUTO']:
                    classification_info['display_name'] = 'Reverse Convertible'
                    classification_info['additional_info'] = 'High coupon with potential equity delivery'
        
        # Leverage Products (HL****)
        elif second_char == 'L':
            classification_info.update({
                'icon': '⚡',
                'display_name': 'Leverage Product',
                'additional_info': 'Leveraged exposure to underlying asset'
            })
            
            # Extract leverage type
            if len(cfi_code) >= 3:
                leverage_type = cfi_code[2]
                if leverage_type == 'T':
                    classification_info['display_name'] = 'Turbo Warrant'
                    classification_info['additional_info'] = 'Knock-out leverage product'
                elif leverage_type == 'C':
                    classification_info['display_name'] = 'Call Warrant'
                elif leverage_type == 'P':
                    classification_info['display_name'] = 'Put Warrant'
        
        # Warrants (HW****)
        elif second_char == 'W':
            classification_info.update({
                'icon': '📜',
                'display_name': 'Structured Warrant',
                'additional_info': 'Complex warrant with structured features'
            })
            
            # Extract warrant specifics
            if firds_data.get('DerivInstrmAttrbts_OptnTp'):
                option_type = firds_data['DerivInstrmAttrbts_OptnTp']
                if option_type == 'CALL':
                    classification_info['display_name'] = 'Call Warrant'
                elif option_type == 'PUTO':
                    classification_info['display_name'] = 'Put Warrant'
        
        # Notes (HN****)
        elif second_char == 'N':
            classification_info.update({
                'icon': '📝',
                'display_name': 'Structured Note',
                'additional_info': 'Note with embedded derivative features'
            })
        
        # Structured Securities (HS****)
        elif second_char == 'S':
            classification_info.update({
                'icon': '🔗',
                'display_name': 'Structured Security',
                'additional_info': 'Security with complex payoff structure'
            })
    
    # Extract common structured product details
    
    # Underlying asset information
    underlying_details = []
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
        underlying_isin = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']
        classification_info['structured_details']['underlying_isin'] = underlying_isin
        underlying_details.append(f'Single: {underlying_isin}')
    
    if firds_data.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
        basket_isins = firds_data['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
        if isinstance(basket_isins, list) and len(basket_isins) > 0:
            classification_info['structured_details']['basket_size'] = len(basket_isins)
            underlying_details.append(f'Basket ({len(basket_isins)} assets)')
        elif isinstance(basket_isins, str):
            underlying_details.append(f'Basket: {basket_isins}')
    
    if underlying_details:
        classification_info['structured_details']['underlying_summary'] = ' | '.join(underlying_details)
    
    # Barrier information
    if firds_data.get('DerivInstrmAttrbts_StrkPric'):
        strike_price = firds_data['DerivInstrmAttrbts_StrkPric']
        classification_info['structured_details']['strike_barrier'] = strike_price
    
    # Settlement information  
    if firds_data.get('DerivInstrmAttrbts_DlvryTp'):
        settlement_type = firds_data['DerivInstrmAttrbts_DlvryTp']
        classification_info['structured_details']['settlement'] = settlement_type
    
    # Expiration
    if firds_data.get('DerivInstrmAttrbts_XpryDt'):
        expiry_date = firds_data['DerivInstrmAttrbts_XpryDt']
        classification_info['structured_details']['expiry_date'] = expiry_date
    
    return classification_info


def _format_type_specific_attributes(instrument):
    """Format instrument type-specific attributes from FIRDS data"""
    if not instrument.firds_data:
        return ""
    
    if not isinstance(instrument.firds_data, dict):
        return ""
    
    firds = instrument.firds_data
    details = []
    
    # Equity-specific attributes
    if instrument.instrument_type == "equity":
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            details.append(f"[cyan]Underlying ISIN:[/cyan] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']}")
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
            details.append(f"[cyan]Underlying Index:[/cyan] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']}")
    
    # Debt-specific attributes  
    elif instrument.instrument_type == "debt":
        if firds.get('DebtInstrmAttrbts_MtrtyDt'):
            details.append(f"[cyan]Maturity Date:[/cyan] {firds['DebtInstrmAttrbts_MtrtyDt']}")
        if firds.get('DebtInstrmAttrbts_DebtSnrty'):
            seniority_map = {'SNDB': 'Senior', 'SUBR': 'Subordinated', 'MZZN': 'Mezzanine'}
            seniority = seniority_map.get(firds['DebtInstrmAttrbts_DebtSnrty'], firds['DebtInstrmAttrbts_DebtSnrty'])
            details.append(f"[cyan]Debt Seniority:[/cyan] {seniority}")
        if firds.get('DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm'):
            details.append(f"[cyan]Reference Rate:[/cyan] {firds['DebtInstrmAttrbts_IntrstRate_Fltg_RefRate_Nm']}")
        if firds.get('DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd'):
            details.append(f"[cyan]Spread:[/cyan] {firds['DebtInstrmAttrbts_IntrstRate_Fltg_BsisPtSprd']} bps")
    
    # Future-specific attributes
    elif instrument.instrument_type == "future":
        # Contract expiration (using actual field name from FIRDS)
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            details.append(f"[bright_yellow]📅 Expiration Date:[/bright_yellow] {firds['DerivInstrmAttrbts_XpryDt']}")
        
        # Settlement type (using actual field name from FIRDS)
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            delivery_type = firds['DerivInstrmAttrbts_DlvryTp']
            if delivery_type == 'CASH':
                details.append(f"[bright_yellow]💰 Settlement:[/bright_yellow] Cash Settlement")
            elif delivery_type == 'PHYS':
                details.append(f"[bright_yellow]📦 Settlement:[/bright_yellow] Physical Delivery")
            else:
                details.append(f"[bright_yellow]🚚 Settlement:[/bright_yellow] {delivery_type}")
        
        # Contract specifications (using actual field name from FIRDS)
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            multiplier = firds['DerivInstrmAttrbts_PricMltplr']
            details.append(f"[bright_yellow]⚖️ Price Multiplier:[/bright_yellow] {multiplier}")
        
        # Commodity classification - determine commodity type and display appropriately
        commodity_info = _get_commodity_classification(firds)
        if commodity_info:
            details.append(f"[bright_yellow]{commodity_info['icon']} Commodity Type:[/bright_yellow] {commodity_info['display_name']}")
            
            # Add additional commodity details if available
            if commodity_info['additional_info']:
                details.append(f"[bright_yellow]📝 Details:[/bright_yellow] {commodity_info['additional_info']}")
        
        # Underlying instrument information
        underlying_details = []
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'):
            underlying_details.append(f"ISIN: {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN']}")
        
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
            underlying_details.append(f"Index: {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']}")
        
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val'):
            term_val = firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Val']
            term_unit = firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_Term_Unit', '')
            if term_unit == 'MNTH':
                term_display = f"{term_val} Month{'s' if int(term_val) != 1 else ''}"
            else:
                term_display = f"{term_val} {term_unit}"
            underlying_details.append(f"Term: {term_display}")
        
        if underlying_details:
            details.append(f"[bright_yellow]🔗 Underlying:[/bright_yellow] {' | '.join(underlying_details)}")
        
        # Final price type information
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp'):
            price_type = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_FnlPricTp']
            price_display = 'Exchange Official' if price_type == 'EXOF' else 'Other' if price_type == 'OTHR' else price_type
            details.append(f"[bright_yellow]💹 Price Type:[/bright_yellow] {price_display}")
    
    # Option-specific attributes
    elif instrument.instrument_type == "option":
        # Basic option information
        if firds.get('DerivInstrmAttrbts_OptnTp'):
            option_type = 'Call' if firds['DerivInstrmAttrbts_OptnTp'] == 'CALL' else 'Put' if firds['DerivInstrmAttrbts_OptnTp'] == 'PUTO' else firds['DerivInstrmAttrbts_OptnTp']
            option_icon = '📈' if option_type == 'Call' else '📉'
            details.append(f"[magenta]{option_icon} Option Type:[/magenta] {option_type}")
        
        # Strike price from processed attributes (preferred) or raw FIRDS (fallback)
        if instrument.processed_attributes and isinstance(instrument.processed_attributes, dict):
            processed = instrument.processed_attributes
            if processed.get('strike_price'):
                strike_info = processed['strike_price']
                strike_details = []
                
                if isinstance(strike_info, dict):
                    if strike_info.get('percentage'):
                        strike_details.append(f"{strike_info['percentage']}%")
                    if strike_info.get('monetary_amount'):
                        amount = strike_info['monetary_amount']
                        sign = strike_info.get('monetary_sign', '')
                        # Only display sign if it's a proper monetary sign (not "true"/"false")
                        if sign and sign.lower() not in ['true', 'false']:
                            strike_details.append(f"{sign}{amount} {instrument.currency or ''}")
                        else:
                            strike_details.append(f"{amount} {instrument.currency or ''}")
                    if strike_info.get('basis_points'):
                        strike_details.append(f"{strike_info['basis_points']} bps")
                else:
                    # Simple strike price value
                    strike_details.append(f"{strike_info} {instrument.currency or ''}")
                
                if strike_details:
                    details.append(f"[magenta]🎯 Strike Price:[/magenta] {' | '.join(strike_details)}")
        
        # Fallback to raw FIRDS data if no processed strike price
        elif firds.get('DerivInstrmAttrbts_StrkPric'):
            basic_strike = firds['DerivInstrmAttrbts_StrkPric']
            if isinstance(basic_strike, (int, float)):
                details.append(f"[magenta]🎯 Strike Price:[/magenta] {basic_strike} {instrument.currency or ''}")
        
        # Exercise style (American/European)
        if firds.get('DerivInstrmAttrbts_OptnExrcStyle'):
            exercise_style = 'American' if firds['DerivInstrmAttrbts_OptnExrcStyle'] == 'AMER' else 'European' if firds['DerivInstrmAttrbts_OptnExrcStyle'] == 'EURO' else firds['DerivInstrmAttrbts_OptnExrcStyle']
            exercise_icon = '🇺🇸' if exercise_style == 'American' else '🇪🇺' if exercise_style == 'European' else '⚙️'
            details.append(f"[magenta]{exercise_icon} Exercise Style:[/magenta] {exercise_style}")
        
        # Expiration details
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            details.append(f"[magenta]📅 Expiration Date:[/magenta] {firds['DerivInstrmAttrbts_XpryDt']}")
        
        # Delivery/Settlement
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            settlement = 'Physical Delivery' if firds['DerivInstrmAttrbts_DlvryTp'] == 'PHYS' else 'Cash Settlement'
            settlement_icon = '📦' if firds['DerivInstrmAttrbts_DlvryTp'] == 'PHYS' else '�'
            details.append(f"[magenta]{settlement_icon} Settlement:[/magenta] {settlement}")
        
        # Underlying instrument details
        underlying_parts = []
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            underlying_parts.append(f"ISIN: {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']}")
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
            underlying_parts.append(f"Index: {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']}")
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN'):
            underlying_parts.append(f"Index ISIN: {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_ISIN']}")
        
        if underlying_parts:
            details.append(f"[magenta]🔗 Underlying:[/magenta] {' | '.join(underlying_parts)}")
        
        # Interest rate derivatives information
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx'):
            interest_parts = [f"Index: {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx']}"]
            
            if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val') and firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit'):
                term_val = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Val']
                term_unit = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_Term_Unit']
                interest_parts.append(f"Term: {term_val} {term_unit}")
            
            details.append(f"[magenta]💰 Interest Rate:[/magenta] {' | '.join(interest_parts)}")
        
        # FX-specific information
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy'):
            details.append(f"[magenta]💱 Other Currency:[/magenta] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy']}")
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp'):
            details.append(f"[magenta]💱 FX Type:[/magenta] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_FxTp']}")
        
        # Basket underlying (for basket options)
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
            basket_isins = firds['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
            if hasattr(basket_isins, '__len__') and hasattr(basket_isins, '__getitem__') and not isinstance(basket_isins, str) and len(basket_isins) > 0:
                details.append(f"[magenta]� Basket Components:[/magenta] {len(basket_isins)} instruments")
                if len(basket_isins) <= 3:
                    for i, isin in enumerate(basket_isins):
                        details.append(f"[magenta]  └─ Component {i+1}:[/magenta] {isin}")
            elif isinstance(basket_isins, str):
                details.append(f"[magenta]📊 Basket ISIN:[/magenta] {basket_isins}")
    
    # Swap-specific attributes
    elif instrument.instrument_type == "swap":
        # Swap classification and type-specific details
        swap_info = _get_swap_classification(instrument, firds)
        if swap_info:
            details.append(f"[bright_magenta]{swap_info['icon']} Swap Type:[/bright_magenta] {swap_info['display_name']}")
            
            # Add additional swap-specific info
            if swap_info['additional_info']:
                details.append(f"[bright_magenta]📝 Details:[/bright_magenta] {swap_info['additional_info']}")

        
        # Contract expiration
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            details.append(f"[bright_magenta]📅 Expiration Date:[/bright_magenta] {firds['DerivInstrmAttrbts_XpryDt']}")
        
        # Settlement type
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            delivery_type = firds['DerivInstrmAttrbts_DlvryTp']
            if delivery_type == 'CASH':
                details.append(f"[bright_magenta]💰 Settlement:[/bright_magenta] Cash Settlement")
            elif delivery_type == 'PHYS':
                details.append(f"[bright_magenta]📦 Settlement:[/bright_magenta] Physical Delivery")
            elif delivery_type == 'OPTL':
                details.append(f"[bright_magenta]⚙️ Settlement:[/bright_magenta] Optional")
            else:
                details.append(f"[bright_magenta]🚚 Settlement:[/bright_magenta] {delivery_type}")
        
        # Price multiplier
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            multiplier = firds['DerivInstrmAttrbts_PricMltplr']
            details.append(f"[bright_magenta]⚖️ Price Multiplier:[/bright_magenta] {multiplier}")
        
        # Type-specific swap details
        if swap_info and swap_info['swap_details']:
            swap_details = swap_info['swap_details']
            
            # Credit Default Swap details
            if 'basket_isin' in swap_details:
                details.append(f"[bright_magenta]🗂️ Basket ISIN:[/bright_magenta] {swap_details['basket_isin']}")
            
            # Equity Total Return Swap details
            if 'underlying_isin' in swap_details:
                details.append(f"[bright_magenta]🔗 Underlying ISIN:[/bright_magenta] {swap_details['underlying_isin']}")
            
            # FX Swap details
            if 'currency_pair' in swap_details:
                details.append(f"[bright_magenta]💱 Currency Pair:[/bright_magenta] {swap_details['currency_pair']}")
            
            # Interest Rate Swap details
            if 'reference_rate' in swap_details:
                details.append(f"[bright_magenta]📊 Reference Rate:[/bright_magenta] {swap_details['reference_rate']}")
            
            if 'floating_term' in swap_details:
                details.append(f"[bright_magenta]📈 Floating Term:[/bright_magenta] {swap_details['floating_term']}")
            
            # OIS Swap details
            if 'ois_rate' in swap_details:
                details.append(f"[bright_magenta]🏦 OIS Rate:[/bright_magenta] {swap_details['ois_rate']}")
            
            if 'compound_period' in swap_details:
                details.append(f"[bright_magenta]🔄 Compound Period:[/bright_magenta] {swap_details['compound_period']}")
        
        # General underlying instrument information
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            details.append(f"[bright_magenta]🎯 Single Underlying:[/bright_magenta] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']}")
        
        # Index information
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx'):
            details.append(f"[bright_magenta]📋 Index:[/bright_magenta] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Indx']}")
    
    # Structured/Hybrid-specific attributes (H-category)
    elif instrument.instrument_type == "structured":
        # Structured product classification and type-specific details
        structured_info = _get_structured_classification(instrument, firds)
        if structured_info:
            details.append(f"[bright_yellow]{structured_info['icon']} Product Type:[/bright_yellow] {structured_info['display_name']}")
            
            # Add additional structured-specific info
            if structured_info['additional_info']:
                details.append(f"[bright_yellow]📝 Details:[/bright_yellow] {structured_info['additional_info']}")
        
        # Contract expiration
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            details.append(f"[bright_yellow]📅 Expiration Date:[/bright_yellow] {firds['DerivInstrmAttrbts_XpryDt']}")
        
        # Settlement type
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            delivery_type = firds['DerivInstrmAttrbts_DlvryTp']
            if delivery_type == 'CASH':
                details.append(f"[bright_yellow]💰 Settlement:[/bright_yellow] Cash Settlement")
            elif delivery_type == 'PHYS':
                details.append(f"[bright_yellow]📦 Settlement:[/bright_yellow] Physical Delivery")
            else:
                details.append(f"[bright_yellow]🚚 Settlement:[/bright_yellow] {delivery_type}")
        
        # Strike price / Barrier levels
        if firds.get('DerivInstrmAttrbts_StrkPric'):
            strike_price = firds['DerivInstrmAttrbts_StrkPric']
            details.append(f"[bright_yellow]🎯 Strike/Barrier:[/bright_yellow] {strike_price} {instrument.currency or ''}")
        
        # Participation rate / Multiplier
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            multiplier = firds['DerivInstrmAttrbts_PricMltplr']
            details.append(f"[bright_yellow]⚖️ Participation Rate:[/bright_yellow] {multiplier}")
        
        # Type-specific structured details
        if structured_info and structured_info['structured_details']:
            struct_details = structured_info['structured_details']
            
            # Underlying summary
            if 'underlying_summary' in struct_details:
                details.append(f"[bright_yellow]🔗 Underlying:[/bright_yellow] {struct_details['underlying_summary']}")
            
            # Individual underlying ISIN
            if 'underlying_isin' in struct_details:
                details.append(f"[bright_yellow]🎯 Underlying ISIN:[/bright_yellow] {struct_details['underlying_isin']}")
            
            # Basket information
            if 'basket_size' in struct_details:
                details.append(f"[bright_yellow]📊 Basket Size:[/bright_yellow] {struct_details['basket_size']} instruments")
        
        # Option-type information (for warrant-like products)
        if firds.get('DerivInstrmAttrbts_OptnTp'):
            option_type = 'Call' if firds['DerivInstrmAttrbts_OptnTp'] == 'CALL' else 'Put' if firds['DerivInstrmAttrbts_OptnTp'] == 'PUTO' else firds['DerivInstrmAttrbts_OptnTp']
            option_icon = '📈' if option_type == 'Call' else '📉'
            details.append(f"[bright_yellow]{option_icon} Option Component:[/bright_yellow] {option_type}")
        
        # Exercise style for warrant-like products
        if firds.get('DerivInstrmAttrbts_OptnExrcStyle'):
            exercise_style = 'American' if firds['DerivInstrmAttrbts_OptnExrcStyle'] == 'AMER' else 'European' if firds['DerivInstrmAttrbts_OptnExrcStyle'] == 'EURO' else firds['DerivInstrmAttrbts_OptnExrcStyle']
            exercise_icon = '🇺🇸' if exercise_style == 'American' else '🇪🇺' if exercise_style == 'European' else '⚙️'
            details.append(f"[bright_yellow]{exercise_icon} Exercise Style:[/bright_yellow] {exercise_style}")
        
        # Interest rate or coupon information
        if firds.get('DebtInstrmAttrbts_IntrstRate_Fxd'):
            fixed_rate = firds['DebtInstrmAttrbts_IntrstRate_Fxd']
            details.append(f"[bright_yellow]💹 Fixed Coupon:[/bright_yellow] {fixed_rate}%")
        
        # Currency information for quanto products
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy'):
            other_currency = firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_FX_OthrNtnlCcy']
            details.append(f"[bright_yellow]💱 Reference Currency:[/bright_yellow] {other_currency}")
    
    # Forward-specific attributes
    elif instrument.instrument_type == "forward":
        # Forward classification and type-specific details
        forward_info = _get_forward_classification(instrument, firds)
        if forward_info:
            details.append(f"[bright_cyan]{forward_info['icon']} Forward Type:[/bright_cyan] {forward_info['display_name']}")
            
            # Add additional forward-specific info
            if forward_info['additional_info']:
                details.append(f"[bright_cyan]📝 Details:[/bright_cyan] {forward_info['additional_info']}")
        
        # Contract expiration
        if firds.get('DerivInstrmAttrbts_XpryDt'):
            details.append(f"[bright_cyan]📅 Expiration Date:[/bright_cyan] {firds['DerivInstrmAttrbts_XpryDt']}")
        
        # Settlement type
        if firds.get('DerivInstrmAttrbts_DlvryTp'):
            delivery_type = firds['DerivInstrmAttrbts_DlvryTp']
            if delivery_type == 'CASH':
                details.append(f"[bright_cyan]💰 Settlement:[/bright_cyan] Cash Settlement")
            elif delivery_type == 'PHYS':
                details.append(f"[bright_cyan]📦 Settlement:[/bright_cyan] Physical Delivery")
            else:
                details.append(f"[bright_cyan]🚚 Settlement:[/bright_cyan] {delivery_type}")
        
        # Price multiplier
        if firds.get('DerivInstrmAttrbts_PricMltplr'):
            multiplier = firds['DerivInstrmAttrbts_PricMltplr']
            details.append(f"[bright_cyan]⚖️ Price Multiplier:[/bright_cyan] {multiplier}")
        
        # Type-specific forward details
        if forward_info and forward_info['forward_details']:
            forward_details = forward_info['forward_details']
            
            # Equity Forward details
            if 'basket_isin' in forward_details:
                details.append(f"[bright_cyan]📦 Basket ISIN:[/bright_cyan] {forward_details['basket_isin']}")
            
            # FX Forward details
            if 'currency_pair' in forward_details:
                details.append(f"[bright_cyan]💱 Currency Pair:[/bright_cyan] {forward_details['currency_pair']}")
            
            if 'fx_type' in forward_details:
                details.append(f"[bright_cyan]🔄 FX Type:[/bright_cyan] {forward_details['fx_type']}")
            
            # Rate Forward details
            if 'underlying_isin' in forward_details:
                details.append(f"[bright_cyan]🎯 Underlying ISIN:[/bright_cyan] {forward_details['underlying_isin']}")
            
            if 'forward_term' in forward_details:
                details.append(f"[bright_cyan]📈 Forward Term:[/bright_cyan] {forward_details['forward_term']}")
        
        # Interest rate information for rate forwards
        if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx'):
            details.append(f"[bright_cyan]📊 Interest Rate Index:[/bright_cyan] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Intrst_IntrstRate_RefRate_Indx']}")
        
        # General underlying instrument information (single ISIN)
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN'):
            details.append(f"[bright_cyan]🔗 Single Underlying:[/bright_cyan] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_ISIN']}")
        
        # Index/reference rate information
        if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm'):
            details.append(f"[bright_cyan]📋 Reference Rate:[/bright_cyan] {firds['DerivInstrmAttrbts_UndrlygInstrm_Sngl_Indx_Nm_RefRate_Nm']}")
    
    # Other derivative types
    elif instrument.instrument_type == "convertible":
        if firds.get('DerivInstrmAttrbts_XprtnDt'):
            details.append(f"[green]📅 Expiration Date:[/green] {firds['DerivInstrmAttrbts_XprtnDt']}")
        if firds.get('DerivInstrmAttrbts_PhysSttlm'):
            settlement = 'Physical' if firds['DerivInstrmAttrbts_PhysSttlm'] == 'PHYS' else 'Cash'
            details.append(f"[green]Settlement:[/green] {settlement}")
    
    # Energy commodity derivatives (Oil, Gas, etc.)
    if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct'):
        details.append(f"[bright_green]⛽ Energy Base Product:[/bright_green] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_BasePdct']}")
    if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct'):
        details.append(f"[bright_green]🛢️  Oil Sub Product:[/bright_green] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Nrgy_Oil_SubPdct']}")
    
    # Agricultural commodities
    if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrainOilSeed_BasePdct'):
        details.append(f"[bright_green]🌾 Agricultural Base:[/bright_green] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Agrcltrl_GrainOilSeed_BasePdct']}")
    
    # Metal commodities
    if firds.get('DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct'):
        details.append(f"[bright_green]🥇 Metal Base Product:[/bright_green] {firds['DerivInstrmAttrbts_AsstClssSpcfcAttrbts_Cmmdty_Pdct_Metl_NonPrcs_BasePdct']}")
    
    # Underlying basket information (for basket derivatives)
    if firds.get('DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN'):
        basket_isins = firds['DerivInstrmAttrbts_UndrlygInstrm_Bskt_ISIN']
        if hasattr(basket_isins, '__len__') and hasattr(basket_isins, '__getitem__') and not isinstance(basket_isins, str) and len(basket_isins) > 0:
            details.append(f"[bright_blue]📊 Basket Components:[/bright_blue] {len(basket_isins)} instruments")
            # Show first few ISINs if not too many
            if len(basket_isins) <= 3:
                for i, isin in enumerate(basket_isins):
                    details.append(f"[bright_blue]  └─ Component {i+1}:[/bright_blue] {isin}")
        elif isinstance(basket_isins, str):
            details.append(f"[bright_blue]📊 Basket ISIN:[/bright_blue] {basket_isins}")
    
    # Additional derivative contract details (for derivatives that aren't futures/options - they handle it themselves)
    if firds.get('DerivInstrmAttrbts_DlvryTp') and instrument.instrument_type not in ['future', 'option']:
        delivery_type = firds['DerivInstrmAttrbts_DlvryTp']
        delivery_icon = '🚚' if delivery_type == 'PHYS' else '💱'
        details.append(f"[cyan]{delivery_icon} Delivery Type:[/cyan] {delivery_type}")
    
    # Contract size and unit information
    if firds.get('DerivInstrmAttrbts_CntrcSz'):
        details.append(f"[cyan]📏 Contract Size:[/cyan] {firds['DerivInstrmAttrbts_CntrcSz']}")
    
    if firds.get('DerivInstrmAttrbts_UnitOfMsr'):
        details.append(f"[cyan]📐 Unit of Measure:[/cyan] {firds['DerivInstrmAttrbts_UnitOfMsr']}")
    
    return "\n".join(details)


def _format_legal_entity_panel(entity):
    """Format legal entity information"""
    return f"""[bold white]{entity.name}[/bold white]
[cyan]LEI:[/cyan] {entity.lei}
[cyan]Jurisdiction:[/cyan] {entity.jurisdiction}
[cyan]Legal Form:[/cyan] {entity.legal_form}
[cyan]Status:[/cyan] [bold green]{entity.status}[/bold green]
[cyan]BIC:[/cyan] {entity.bic or 'N/A'}
[cyan]Managing LOU:[/cyan] {entity.managing_lou}"""


def _format_trading_venues_table(venues):
    """Format trading venues as an adaptive table showing only meaningful data columns"""
    if not venues:
        return "No trading venues available"
    
    from rich.table import Table
    from marketdata_api.database.session import get_session
    from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
    
    # First pass: analyze what data is actually available
    venue_data = []
    has_mic_data = False
    has_admission = False
    has_termination = False
    
    with get_session() as session:
        for venue in venues[:10]:  # Limit to first 10
            # Get MIC code - try mic_code field first, then fall back to venue_id
            mic_lookup_code = venue.mic_code or venue.venue_id
            
            # Direct MIC lookup (more reliable than relationship)
            mic_data = None
            if mic_lookup_code:
                mic_data = session.query(MarketIdentificationCode).filter(
                    MarketIdentificationCode.mic == mic_lookup_code
                ).first()
            
            # Build venue row data
            row_data = {
                'mic_code': venue.venue_id or "N/A",
                'market_name': "N/A",
                'market_type': "N/A", 
                'country': "N/A",
                'status': "N/A",
                'first_trade': "N/A",
                'admission_date': "N/A",
                'termination_date': "N/A"
            }
            
            # Populate MIC data if found
            if mic_data:
                has_mic_data = True
                row_data['market_name'] = mic_data.market_name or mic_data.acronym or "N/A"
                row_data['market_type'] = mic_data.operation_type.value if mic_data.operation_type else "N/A"
                row_data['country'] = mic_data.iso_country_code or "N/A"
                # Store raw status for later color formatting
                row_data['status'] = mic_data.status.value if mic_data.status else "N/A"
                row_data['status_raw'] = row_data['status']  # Keep raw for comparison
            else:
                # Fallback to venue-specific names
                row_data['market_name'] = venue.venue_full_name or venue.venue_short_name or "N/A"
            
            # Format first trade date
            if venue.first_trade_date:
                row_data['first_trade'] = venue.first_trade_date.strftime("%Y-%m-%d")
            
            # Check for additional dates in processed attributes or promoted fields
            if venue.admission_approval_date:
                row_data['admission_date'] = venue.admission_approval_date.strftime("%Y-%m-%d")
                has_admission = True
            elif venue.request_for_admission_date:
                row_data['admission_date'] = venue.request_for_admission_date.strftime("%Y-%m-%d") 
                has_admission = True
            
            if venue.termination_date:
                row_data['termination_date'] = venue.termination_date.strftime("%Y-%m-%d")
                has_termination = True
            
            venue_data.append(row_data)
    
    # Create adaptive table with only meaningful columns
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("MIC", style="bold cyan", width=4)
    table.add_column("Market Name", style="white", width=32)
    
    # Only add MIC-derived columns if we have MIC data
    if has_mic_data:
        table.add_column("Country", style="bright_green", width=7)
        table.add_column("Status", style="magenta", width=8)
    
    # Always show first trade (it has data)
    table.add_column("First Trade", style="green", width=11)
    
    # Only add date columns if they have actual data
    if has_admission:
        table.add_column("Admission", style="blue", width=11)
    if has_termination:
        table.add_column("Termination", style="red", width=11)
    
    # Add rows with adaptive columns
    for row_data in venue_data:
        # Truncate long market names
        market_name = row_data['market_name']
        if len(market_name) > 30:
            market_name = market_name[:27] + "..."
        
        # Build row based on which columns we're showing
        row = [
            row_data['mic_code'],
            market_name
        ]
        
        if has_mic_data:
            # Simple status display without color codes (tables strip formatting)
            status = row_data['status_raw'] if 'status_raw' in row_data else row_data['status']
            status_display = status if status != "N/A" else "N/A"
                
            row.extend([row_data['country'], status_display])
        
        row.append(row_data['first_trade'])
        
        if has_admission:
            row.append(row_data['admission_date'])
        if has_termination:
            row.append(row_data['termination_date'])
        
        table.add_row(*row)
    
    # Add summary
    total_venues = len(venues)
    if total_venues > 10:
        table.caption = f"Showing first 10 of {total_venues} trading venues"
    elif not has_mic_data:
        table.caption = "Note: MIC registry data not linked for these venues"
    
    # Render table to string for panel
    from rich.console import Console
    from io import StringIO
    temp_console = Console(file=StringIO(), width=120)
    temp_console.print(table)
    return temp_console.file.getvalue()


def _format_figi_mappings(figis):
    """Format FIGI mapping information"""
    details = []
    for i, figi in enumerate(figis[:5]):  # Limit to 5 FIGIs
        details.append(f"[bold]FIGI {i+1}:[/bold]")
        details.append(f"  [cyan]FIGI:[/cyan] {figi.figi or 'N/A'}")
        if figi.ticker:
            details.append(f"  [cyan]Ticker:[/cyan] {figi.ticker}")
        if figi.security_type:
            details.append(f"  [cyan]Security Type:[/cyan] {figi.security_type}")
        if figi.market_sector:
            details.append(f"  [cyan]Market Sector:[/cyan] {figi.market_sector}")
        details.append("")  # Empty line between FIGIs
    
    return "\n".join(details)


def _format_transparency_data(calculations):
    """Format transparency calculation data"""
    if not calculations:
        return "No transparency data available"
    
    details = []
    for calc in calculations[:3]:  # Show latest 3 calculations
        liquidity = "High" if calc.liquidity else "Low" if calc.liquidity is False else "Unknown"
        liquidity_color = "green" if calc.liquidity else "red" if calc.liquidity is False else "yellow"
        
        details.append(f"[cyan]Period:[/cyan] {calc.from_date} to {calc.to_date}")
        details.append(f"[cyan]Liquidity:[/cyan] [{liquidity_color}]{liquidity}[/{liquidity_color}]")
        if calc.total_transactions_executed:
            details.append(f"[cyan]Transactions:[/cyan] {calc.total_transactions_executed:,}")
        if calc.total_volume_executed:
            details.append(f"[cyan]Volume:[/cyan] {calc.total_volume_executed:,.2f}")
        details.append("")
    
    return "\n".join(details)


def _get_cfi_description(cfi_code):
    """Get human-readable CFI code description"""
    if not cfi_code or len(cfi_code) < 1:
        return "Unknown"
    
    # Basic CFI code mappings
    cfi_descriptions = {
        'E': 'Equities',
        'D': 'Debt Instruments', 
        'C': 'Collective Investment',
        'F': 'Futures',
        'O': 'Options',
        'H': 'Hybrid Securities',
        'I': 'Interest Rate Derivatives',
        'J': 'Forwards',
        'R': 'Rights',
        'S': 'Swaps'
    }
    
    return cfi_descriptions.get(cfi_code[0], f"Type {cfi_code[0]}")