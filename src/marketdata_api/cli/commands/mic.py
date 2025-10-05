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
@click.option("--full", is_flag=True, help="Show complete details including related instruments and statistics")
@click.pass_context
@handle_database_error
def get_mic(ctx, mic_code, full):
    """Get detailed MIC information with enhanced analysis"""
    try:
        from marketdata_api.database.session import get_session
        from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
        
        with console.status(f"[bold green]Looking up MIC {mic_code}..."):
            with get_session() as session:
                mic = (
                    session.query(MarketIdentificationCode).filter_by(mic=mic_code.upper()).first()
                )

                if not mic:
                    console.print(f"[red]❌ MIC not found: {mic_code}[/red]")
                    return

                # Display comprehensive MIC analysis
                _display_mic_rich(mic, session, full)

    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


def _display_mic_rich(mic, session, show_full=False):
    """Display MIC information with rich formatting and comprehensive details"""
    from rich.columns import Columns
    from rich.text import Text
    
    # Main MIC panel
    main_details = _format_main_mic_panel(mic)
    console.print(Panel(main_details, title=f"🏛️ {mic.mic}", border_style="blue"))
    
    # Market Details Panel  
    market_details = _format_market_details_panel(mic)
    if market_details.strip():
        console.print(Panel(market_details, title="🌍 Market Information", border_style="green"))
    
    if show_full:
        # Related instruments and statistics
        instruments_info = _format_related_instruments_info(mic, session)
        if instruments_info.strip():
            console.print(Panel(instruments_info, title="📊 Market Activity", border_style="yellow"))
        
        # Related MICs (segment MICs under this operating MIC)
        related_mics = _format_related_mics(mic, session)
        if related_mics.strip():
            console.print(Panel(related_mics, title="🔗 Related MICs", border_style="cyan"))
        
        # LEI Entity Information (if available)
        if mic.lei:
            entity_info = _format_lei_entity_info(mic, session)
            if entity_info.strip():
                console.print(Panel(entity_info, title="🏢 Legal Entity Information", border_style="magenta"))


def _format_main_mic_panel(mic):
    """Format the main MIC identification panel"""
    # Status indicators
    status_icons = []
    if mic.status and mic.status.value == "ACTIVE":
        status_icons.append("✅ Active")
    elif mic.status:
        status_icons.append(f"⚠️ {mic.status.value}")
    
    if mic.operation_type:
        op_type = mic.operation_type.value
        if op_type == "OPRT":
            status_icons.append("🏛️ Operating MIC")
        elif op_type == "SGMT":
            status_icons.append("📋 Segment MIC")
        else:
            status_icons.append(f"🏷️ {op_type}")
    
    if mic.lei:
        status_icons.append("🔍 LEI Available")
    
    status_line = " • ".join(status_icons) if status_icons else "ℹ️ Basic Information"
    
    return f"""[bold white]{mic.market_name or 'N/A'}[/bold white]
[dim]{mic.legal_entity_name or 'Market operator information not available'}[/dim]

[cyan]MIC Code:[/cyan] [bold]{mic.mic}[/bold]
[cyan]Country:[/cyan] [bold green]{mic.iso_country_code}[/bold green]
[cyan]City:[/cyan] {mic.city or 'N/A'}
[cyan]Status:[/cyan] [bold]{mic.status.value if mic.status else 'N/A'}[/bold]
[cyan]Type:[/cyan] {mic.operation_type.value if mic.operation_type else 'N/A'}

[dim]{status_line}[/dim]"""


def _format_market_details_panel(mic):
    """Format market and operational details"""
    details = []
    
    if mic.operating_mic and mic.operating_mic != mic.mic:
        details.append(f"[cyan]Operating MIC:[/cyan] {mic.operating_mic}")
        details.append(f"[dim]This is a segment under the {mic.operating_mic} market[/dim]")
    elif mic.operation_type and mic.operation_type.value == "OPRT":
        details.append(f"[cyan]Operating MIC:[/cyan] {mic.mic} (self)")
        details.append(f"[dim]This is a primary operating market[/dim]")
    
    if mic.lei:
        details.append(f"[cyan]Legal Entity Identifier:[/cyan] {mic.lei}")
    
    # Market category and type information
    if mic.market_category_code:
        category_desc = _get_market_category_description(mic.market_category_code.value)
        details.append(f"[cyan]Market Category:[/cyan] {mic.market_category_code.value} - {category_desc}")
    
    # Add creation/modification dates if available
    if hasattr(mic, 'creation_date') and mic.creation_date:
        details.append(f"[cyan]Created:[/cyan] {mic.creation_date.strftime('%Y-%m-%d') if hasattr(mic.creation_date, 'strftime') else mic.creation_date}")
    
    if hasattr(mic, 'last_update_date') and mic.last_update_date:
        details.append(f"[cyan]Last Updated:[/cyan] {mic.last_update_date.strftime('%Y-%m-%d') if hasattr(mic.last_update_date, 'strftime') else mic.last_update_date}")
    
    return "\n".join(details)


def _format_related_instruments_info(mic, session):
    """Format information about instruments traded on this MIC"""
    try:
        from marketdata_api.models.sqlite.instrument import Instrument, TradingVenue
        
        # Count instruments by type that trade on this MIC
        instrument_counts = session.query(
            Instrument.instrument_type,
            session.query(TradingVenue).filter(TradingVenue.mic_code == mic.mic).count()
        ).join(TradingVenue).filter(TradingVenue.mic_code == mic.mic).group_by(
            Instrument.instrument_type
        ).all()
        
        if not instrument_counts:
            return "No instrument data available"
        
        details = []
        total_instruments = sum(count for _, count in instrument_counts)
        details.append(f"[cyan]Total Instruments:[/cyan] {total_instruments}")
        
        # Breakdown by type
        for inst_type, count in sorted(instrument_counts, key=lambda x: x[1], reverse=True):
            if count > 0:
                details.append(f"  [cyan]{inst_type.title() if inst_type else 'Unknown'}:[/cyan] {count}")
        
        # Get some recent trading venues as examples
        recent_venues = session.query(TradingVenue).filter(
            TradingVenue.mic_code == mic.mic
        ).order_by(TradingVenue.first_trade_date.desc()).limit(3).all()
        
        if recent_venues:
            details.append(f"\n[cyan]Recent Trading Activity:[/cyan]")
            for venue in recent_venues:
                if venue.instrument and venue.first_trade_date:
                    details.append(f"  {venue.instrument.full_name or venue.instrument.isin} (since {venue.first_trade_date})")
        
        return "\n".join(details)
        
    except Exception as e:
        return f"Error loading instrument data: {str(e)}"


def _format_related_mics(mic, session):
    """Format related MICs (segments under this operating MIC or parent MIC)"""
    try:
        from marketdata_api.models.sqlite.market_identification_code import MarketIdentificationCode
        
        details = []
        
        # If this is an operating MIC, find its segments
        if mic.operation_type and mic.operation_type.value == "OPRT":
            segments = session.query(MarketIdentificationCode).filter(
                MarketIdentificationCode.operating_mic == mic.mic,
                MarketIdentificationCode.mic != mic.mic  # Exclude self
            ).all()
            
            if segments:
                details.append(f"[cyan]Market Segments ({len(segments)}):[/cyan]")
                for segment in segments[:5]:  # Show first 5
                    status_indicator = "🟢" if segment.status and segment.status.value == "ACTIVE" else "🔴"
                    details.append(f"  {status_indicator} {segment.mic} - {segment.market_name or 'N/A'}")
                
                if len(segments) > 5:
                    details.append(f"  ... and {len(segments) - 5} more segments")
        
        # If this is a segment, show parent operating MIC
        elif mic.operating_mic and mic.operating_mic != mic.mic:
            parent_mic = session.query(MarketIdentificationCode).filter(
                MarketIdentificationCode.mic == mic.operating_mic
            ).first()
            
            if parent_mic:
                details.append(f"[cyan]Parent Operating MIC:[/cyan]")
                status_indicator = "🟢" if parent_mic.status and parent_mic.status.value == "ACTIVE" else "🔴"
                details.append(f"  {status_indicator} {parent_mic.mic} - {parent_mic.market_name or 'N/A'}")
                
                # Show sibling segments
                siblings = session.query(MarketIdentificationCode).filter(
                    MarketIdentificationCode.operating_mic == mic.operating_mic,
                    MarketIdentificationCode.mic != mic.mic  # Exclude self
                ).limit(3).all()
                
                if siblings:
                    details.append(f"\n[cyan]Sibling Segments:[/cyan]")
                    for sibling in siblings:
                        status_indicator = "🟢" if sibling.status and sibling.status.value == "ACTIVE" else "🔴"
                        details.append(f"  {status_indicator} {sibling.mic} - {sibling.market_name or 'N/A'}")
        
        return "\n".join(details)
        
    except Exception as e:
        return f"Error loading related MICs: {str(e)}"


def _format_lei_entity_info(mic, session):
    """Format LEI entity information if available"""
    try:
        from marketdata_api.models.sqlite.legal_entity import LegalEntity
        
        if not mic.lei:
            return ""
        
        entity = session.query(LegalEntity).filter(LegalEntity.lei == mic.lei).first()
        
        if not entity:
            return f"LEI {mic.lei} not found in database"
        
        details = []
        details.append(f"[cyan]Legal Name:[/cyan] {entity.name}")
        details.append(f"[cyan]Jurisdiction:[/cyan] {entity.jurisdiction}")
        details.append(f"[cyan]Legal Form:[/cyan] {entity.legal_form}")
        details.append(f"[cyan]Status:[/cyan] {entity.status}")
        
        if entity.bic:
            bic_codes = entity.bic.split(',')[:3]  # Show first 3 BIC codes
            details.append(f"[cyan]BIC Codes:[/cyan] {', '.join(bic_codes)}")
        
        if hasattr(entity, 'addresses') and entity.addresses:
            hq_address = next((addr for addr in entity.addresses if addr.type == 'headquarters'), None)
            if hq_address:
                details.append(f"[cyan]Headquarters:[/cyan] {hq_address.city}, {hq_address.country}")
        
        return "\n".join(details)
        
    except Exception as e:
        return f"Error loading LEI entity data: {str(e)}"


def _get_market_category_description(category_code):
    """Get description for market category code"""
    descriptions = {
        'RMKT': 'Regulated Market',
        'MLTF': 'Multilateral Trading Facility',
        'SMKT': 'SME Growth Market', 
        'MKTM': 'Market Maker',
        'OTCF': 'OTC Facility',
        'SINT': 'Systematic Internaliser',
        'APPA': 'Approved Publication Arrangement'
    }
    return descriptions.get(category_code, 'Unknown Category')


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
