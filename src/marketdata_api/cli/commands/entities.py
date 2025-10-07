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
@click.option("--country", help="Filter by jurisdiction code")
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
                    query = query.filter_by(jurisdiction=country.upper())

                # Extract data within session context
                entities_data = []
                for entity in query.limit(limit).all():
                    entities_data.append(
                        {
                            "lei": entity.lei,
                            "name": entity.name,
                            "jurisdiction": entity.jurisdiction,
                            "status": entity.status,
                        }
                    )

        if not entities_data:
            console.print("[yellow]No legal entities found[/yellow]")
            return

        table = Table(title=f"Legal Entities{f' for {country.upper()}' if country else ''}")
        table.add_column("LEI", style="cyan", no_wrap=True)
        table.add_column("Legal Name", style="green")
        table.add_column("Jurisdiction", style="magenta")
        table.add_column("Status", style="yellow")

        for entity_data in entities_data:
            table.add_row(
                entity_data["lei"],
                (entity_data["name"] or "N/A")[:50]
                + ("..." if len(entity_data["name"] or "") > 50 else ""),
                entity_data["jurisdiction"] or "N/A",
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
@click.option("--full", is_flag=True, help="Show complete details including relationships and addresses")
@click.pass_context
@handle_database_error
def get_entity(ctx, lei, full):
    """Get detailed legal entity information by LEI with comprehensive display"""
    try:
        from marketdata_api.services.sqlite.legal_entity_service import LegalEntityService
        from rich.columns import Columns
        from rich.text import Text
        
        service = LegalEntityService()

        with console.status(f"[bold green]Looking up LEI {lei}..."):
            session, entity = service.get_entity(lei)

        if not entity:
            console.print(f"[red]❌ Legal entity not found: {lei}[/red]")
            return

        # Main entity panel
        _display_entity_rich(entity, full)
        session.close()

    except Exception as e:
        console.print(f"[red]❌ Error: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


@entities.command()
@click.argument("lei")
@click.option("--force", is_flag=True, help="Overwrite existing entity if it exists")
@click.pass_context
@handle_database_error
def create(ctx, lei, force):
    """Create a new legal entity from GLEIF API data"""
    try:
        from marketdata_api.services.sqlite.legal_entity_service import LegalEntityService
        from marketdata_api.database.session import get_session
        
        # Validate LEI format
        if not _validate_lei_format(lei):
            console.print(f"[red]❌ Invalid LEI format: {lei}[/red]")
            console.print("[dim]LEI must be 20 characters: 4 char prefix + 2 char country + 12 char identifier + 2 char checksum[/dim]")
            return
        
        service = LegalEntityService()
        
        # Check if entity already exists
        with console.status(f"[bold blue]Checking if LEI {lei} already exists..."):
            session, existing_entity = service.get_entity(lei)
            if existing_entity and not force:
                session.close()
                console.print(f"[yellow]⚠️  Entity with LEI {lei} already exists[/yellow]")
                console.print("[dim]Use --force to overwrite existing entity[/dim]")
                return
            if session:
                session.close()
        
        # Create or update entity from GLEIF API
        with console.status(f"[bold green]Fetching LEI data from GLEIF API and creating entity..."):
            session, entity = service.create_or_update_entity(lei)
            
        if not entity:
            console.print(f"[red]❌ Failed to create entity for LEI: {lei}[/red]")
            console.print("[dim]LEI may not exist in GLEIF database or API may be unavailable[/dim]")
            return
        
        try:
            # Display the created entity
            action = "Updated" if existing_entity and force else "Created"
            console.print(f"[green]✅ {action} legal entity successfully![/green]")
            console.print()
            
            # Show comprehensive entity details
            _display_entity_rich(entity, show_full=True)
            
        finally:
            session.close()
            
    except Exception as e:
        console.print(f"[red]❌ Error creating entity: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


@entities.command("get-remote")
@click.argument("lei")
@click.option("--include-relationships", "-r", is_flag=True, help="Include parent/child relationships")
@click.pass_context
@handle_database_error
def get_remote(ctx, lei, include_relationships):
    """Get legal entity information directly from GLEIF API (no database storage)"""
    try:
        # Validate LEI format
        if not _validate_lei_format(lei):
            console.print(f"[red]❌ Invalid LEI format: {lei}[/red]")
            console.print("[dim]LEI must be 20 characters: 4 char prefix + 2 char country + 12 char identifier + 2 char checksum[/dim]")
            return
        
        # Import here to avoid issues with module loading
        from marketdata_api.services.gleif import fetch_lei_info
        
        # Fetch basic entity information
        with console.status(f"[bold green]Fetching LEI {lei} from GLEIF API..."):
            gleif_data = fetch_lei_info(lei)
            
        if not gleif_data or 'error' in gleif_data:
            error_msg = gleif_data.get('error', 'Unknown error') if gleif_data else 'No data returned'
            console.print(f"[red]❌ Failed to fetch LEI data: {error_msg}[/red]")
            return
        
        # Display the actual entity data from GLEIF API
        _display_gleif_data_rich(gleif_data)
        
        # Fetch relationship data if requested
        if include_relationships:
            try:
                from marketdata_api.services.gleif import fetch_direct_parent, fetch_ultimate_parent
                console.print()
                with console.status(f"[bold blue]Fetching relationship data..."):
                    # Fetch parent relationships
                    direct_parent_data = fetch_direct_parent(lei)
                    ultimate_parent_data = fetch_ultimate_parent(lei)
                
                _display_gleif_relationships_rich(direct_parent_data, ultimate_parent_data)
            except ImportError:
                console.print("[yellow]⚠️  Relationship data functions not available[/yellow]")
            except Exception as rel_e:
                console.print(f"[red]❌ Error fetching relationships: {str(rel_e)}[/red]")
            
    except Exception as e:
        console.print(f"[red]❌ Error fetching remote data: {str(e)}[/red]")
        if ctx.obj.get("verbose"):
            import traceback
            traceback.print_exc()


def _validate_lei_format(lei):
    """Validate LEI format (20 characters)"""
    return lei and len(lei) == 20 and lei.isalnum()


def _display_gleif_data_rich(gleif_data):
    """Display GLEIF API data with rich formatting"""
    try:
        # Parse GLEIF API response structure
            
        # Use the same mapping approach as the create command
        lei_info = "N/A"
        legal_name = "N/A"
        status = "N/A"
        jurisdiction = "N/A" 
        legal_form = "N/A"
        
        if gleif_data and not gleif_data.get('error'):
            try:
                from marketdata_api.database.model_mapper import map_lei_record
                mapped_data = map_lei_record(gleif_data)
                
                # Extract from the correct nested structure
                lei_record = mapped_data.get('lei_record', {})
                addresses = mapped_data.get('addresses', [])
                registration = mapped_data.get('registration', {})
                
                # Extract mapped information from lei_record
                lei_info = lei_record.get('lei', lei_info)
                legal_name = lei_record.get('name', legal_name)
                status = lei_record.get('status', status)
                jurisdiction = lei_record.get('jurisdiction', jurisdiction)
                legal_form = lei_record.get('legal_form', legal_form)
                
                # Additional fields for richer display
                bic = lei_record.get('bic', None)
                creation_date = lei_record.get('creation_date', None)
                registration_status = lei_record.get('registration_status', None)
                managing_lou = lei_record.get('managing_lou', None)
                
            except Exception as mapping_error:
                console.print(f"[yellow]⚠️  Mapping failed: {str(mapping_error)}[/yellow]")
                import traceback
                traceback.print_exc()
        
        # Display formatted information
        details = f"""[cyan]LEI:[/cyan] [bold]{lei_info}[/bold]
[cyan]Legal Name:[/cyan] [bold white]{legal_name}[/bold white]
[cyan]Status:[/cyan] [bold green]{status}[/bold green] 
[cyan]Jurisdiction:[/cyan] {jurisdiction}
[cyan]Legal Form:[/cyan] {legal_form}

[dim]🌐 Data source: GLEIF API (live data, not stored locally)[/dim]"""
        
        console.print(Panel(details, title=f"� Remote Entity Information", border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]❌ Error displaying GLEIF data: {str(e)}[/red]")


def _display_gleif_relationships_rich(direct_parent_data, ultimate_parent_data):
    """Display GLEIF relationship data with rich formatting"""
    relationship_info = []
    
    # Direct parent information
    if direct_parent_data and 'error' not in direct_parent_data:
        try:
            if 'data' in direct_parent_data:
                data_field = direct_parent_data['data']
                # Handle both list and single object responses
                if hasattr(data_field, '__len__'):
                    data_len = len(data_field)
                    if data_len > 0:
                        parent_data = data_field[0] if hasattr(data_field, '__getitem__') else data_field
                    else:
                        relationship_info.append(f"[cyan]Direct Parent:[/cyan] [dim]No parent relationship records (empty data array)[/dim]")
                        parent_data = None
                else:
                    parent_data = data_field
                
                if parent_data:
                    parent_attrs = parent_data.get('attributes', {})
                    
                    if 'directParent' in parent_attrs:
                        parent_lei = parent_attrs['directParent'].get('lei', 'N/A')
                        parent_name = parent_attrs['directParent'].get('name', 'N/A')
                        relationship_info.append(f"[cyan]Direct Parent:[/cyan] {parent_name} ({parent_lei})")
                    elif 'exceptionCategory' in parent_attrs:
                        exception_cat = parent_attrs['exceptionCategory']
                        exception_reason = parent_attrs.get('exceptionReason', 'Not specified')
                        relationship_info.append(f"[cyan]Direct Parent:[/cyan] [yellow]Exception - {exception_cat}[/yellow]")
                        relationship_info.append(f"[cyan]Reason:[/cyan] {exception_reason}")
                    else:
                        relationship_info.append(f"[cyan]Direct Parent:[/cyan] [dim]No parent information available[/dim]")
            else:
                relationship_info.append(f"[cyan]Direct Parent:[/cyan] [dim]No data field in response[/dim]")
        except Exception as e:
            # For debugging - show what data we actually received
            relationship_info.append(f"[yellow]Debug - Direct parent data type: {type(direct_parent_data)}[/yellow]")
            if hasattr(direct_parent_data, 'keys'):
                relationship_info.append(f"[yellow]Debug - Keys: {list(direct_parent_data.keys())}[/yellow]")
            relationship_info.append(f"[red]Error parsing direct parent data: {str(e)}[/red]")
    else:
        error_msg = direct_parent_data.get('error', 'No direct parent data available') if direct_parent_data else 'No data returned'
        relationship_info.append(f"[cyan]Direct Parent:[/cyan] [dim]{error_msg}[/dim]")
    
    # Ultimate parent information
    if ultimate_parent_data and 'error' not in ultimate_parent_data:
        try:
            if 'data' in ultimate_parent_data:
                data_field = ultimate_parent_data['data']
                # Handle both list and single object responses
                if hasattr(data_field, '__len__'):
                    data_len = len(data_field)
                    if data_len > 0:
                        parent_data = data_field[0] if hasattr(data_field, '__getitem__') else data_field
                    else:
                        relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] [dim]No parent relationship records (empty data array)[/dim]")
                        parent_data = None
                else:
                    parent_data = data_field
                
                if parent_data:
                    parent_attrs = parent_data.get('attributes', {})
                    
                    if 'ultimateParent' in parent_attrs:
                        parent_lei = parent_attrs['ultimateParent'].get('lei', 'N/A')
                        parent_name = parent_attrs['ultimateParent'].get('name', 'N/A')
                        relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] {parent_name} ({parent_lei})")
                    elif 'exceptionCategory' in parent_attrs:
                        exception_cat = parent_attrs['exceptionCategory']
                        exception_reason = parent_attrs.get('exceptionReason', 'Not specified')
                        relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] [yellow]Exception - {exception_cat}[/yellow]")
                        relationship_info.append(f"[cyan]Reason:[/cyan] {exception_reason}")
                    else:
                        relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] [dim]No parent information available[/dim]")
            else:
                relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] [dim]No data field in response[/dim]")
        except Exception as e:
            # For debugging - show what data we actually received
            relationship_info.append(f"[yellow]Debug - Ultimate parent data type: {type(ultimate_parent_data)}[/yellow]")
            if hasattr(ultimate_parent_data, 'keys'):
                relationship_info.append(f"[yellow]Debug - Keys: {list(ultimate_parent_data.keys())}[/yellow]")
            relationship_info.append(f"[red]Error parsing ultimate parent data: {str(e)}[/red]")
    else:
        error_msg = ultimate_parent_data.get('error', 'No ultimate parent data available') if ultimate_parent_data else 'No data returned'
        relationship_info.append(f"[cyan]Ultimate Parent:[/cyan] [dim]{error_msg}[/dim]")
    
    if relationship_info:
        console.print(Panel("\n".join(relationship_info), title="🔗 Corporate Relationships", border_style="cyan"))


def _display_entity_rich(entity, show_full=False):
    """Display legal entity with rich formatting and comprehensive details"""
    from rich.columns import Columns
    from rich.text import Text
    
    # Main entity panel
    main_details = _format_main_entity_panel(entity)
    console.print(Panel(main_details, title=f"🏢 {entity.lei}", border_style="blue"))
    
    # Registration Details Panel  
    registration_details = _format_registration_panel(entity)
    if registration_details.strip():
        console.print(Panel(registration_details, title="📋 Registration Details", border_style="green"))
    
    if show_full:
        # Addresses
        if entity.addresses:
            addresses_display = _format_addresses_table(entity.addresses)
            console.print(Panel(addresses_display, title="🏠 Addresses", border_style="cyan"))
        
        # Corporate Relationships
        if (entity.direct_parent_relation or entity.ultimate_parent_relation or 
            entity.direct_children_relations or entity.ultimate_children_relations):
            relationships_display = _format_relationships_panel(entity)
            console.print(Panel(relationships_display, title="🔗 Corporate Structure", border_style="magenta"))
        
        # Related Instruments
        if hasattr(entity, 'instruments') and entity.instruments:
            instruments_display = _format_related_instruments(entity.instruments)
            console.print(Panel(instruments_display, title="📊 Related Instruments", border_style="yellow"))


def _format_main_entity_panel(entity):
    """Format the main entity identification panel"""
    # Status indicators
    status_icons = []
    if entity.status == "ACTIVE":
        status_icons.append("✅ Active")
    else:
        status_icons.append(f"⚠️ {entity.status}")
    
    if entity.bic:
        status_icons.append("🏦 BIC Available")
    
    if hasattr(entity, 'addresses') and entity.addresses:
        status_icons.append(f"🏠 {len(entity.addresses)} Address(es)")
    
    status_line = " • ".join(status_icons) if status_icons else "ℹ️ Basic Information"
    
    return f"""[bold white]{entity.name}[/bold white]
[dim]{entity.registered_as}[/dim]

[cyan]LEI:[/cyan] [bold]{entity.lei}[/bold]
[cyan]Jurisdiction:[/cyan] [bold green]{entity.jurisdiction}[/bold green]
[cyan]Legal Form:[/cyan] {entity.legal_form}
[cyan]Status:[/cyan] [bold]{entity.status}[/bold]
[cyan]Managing LOU:[/cyan] {entity.managing_lou}

[dim]{status_line}[/dim]"""


def _format_registration_panel(entity):
    """Format registration and regulatory details"""
    details = []
    
    if entity.registration_status:
        details.append(f"[cyan]Registration Status:[/cyan] {entity.registration_status}")
    
    if entity.bic:
        # Handle multiple BIC codes if they exist
        bic_codes = entity.bic.split(',') if ',' in entity.bic else [entity.bic]
        if len(bic_codes) > 3:
            bic_display = f"{', '.join(bic_codes[:3])} + {len(bic_codes) - 3} more"
        else:
            bic_display = ', '.join(bic_codes)
        details.append(f"[cyan]BIC Code(s):[/cyan] {bic_display}")
    
    if entity.next_renewal_date:
        details.append(f"[cyan]Next Renewal:[/cyan] {entity.next_renewal_date.strftime('%Y-%m-%d') if hasattr(entity.next_renewal_date, 'strftime') else entity.next_renewal_date}")
    
    if entity.creation_date:
        details.append(f"[cyan]Created:[/cyan] {entity.creation_date.strftime('%Y-%m-%d') if hasattr(entity.creation_date, 'strftime') else entity.creation_date}")
    
    # Registration details if available
    if hasattr(entity, 'registration') and entity.registration:
        registration = entity.registration
        if registration.initial_date:
            details.append(f"[cyan]Initial Registration:[/cyan] {registration.initial_date.strftime('%Y-%m-%d') if hasattr(registration.initial_date, 'strftime') else registration.initial_date}")
    
    return "\n".join(details)


def _format_addresses_table(addresses):
    """Format addresses in a table"""
    if not addresses:
        return "No addresses available"
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type", style="cyan")
    table.add_column("Address", style="green")
    table.add_column("City", style="yellow")
    table.add_column("Country", style="magenta")
    table.add_column("Postal Code", style="blue")
    
    for addr in addresses:
        table.add_row(
            addr.type.title() if addr.type else "N/A",
            (addr.address_lines or "N/A")[:40] + ("..." if len(addr.address_lines or "") > 40 else ""),
            addr.city or "N/A",
            addr.country or "N/A",
            addr.postal_code or "N/A"
        )
    
    return table


def _format_relationships_panel(entity):
    """Format corporate structure relationships"""
    relationships = []
    
    # Direct parent
    if entity.direct_parent_relation and entity.direct_parent_relation.parent:
        parent = entity.direct_parent_relation.parent
        relationships.append(f"[cyan]Direct Parent:[/cyan] {parent.name} ({parent.lei})")
    
    # Ultimate parent
    if entity.ultimate_parent_relation and entity.ultimate_parent_relation.parent:
        ultimate = entity.ultimate_parent_relation.parent
        relationships.append(f"[cyan]Ultimate Parent:[/cyan] {ultimate.name} ({ultimate.lei})")
    
    # Direct children
    if entity.direct_children_relations:
        children_count = len(entity.direct_children_relations)
        relationships.append(f"[cyan]Direct Subsidiaries:[/cyan] {children_count} entities")
        for i, rel in enumerate(entity.direct_children_relations[:10]):  # Show first 10
            if rel.child:
                relationships.append(f"  └─ {rel.child.name} ({rel.child.lei})")
        if children_count > 10:
            relationships.append(f"  └─ ... and {children_count - 10} more")
    
    # Ultimate children
    if entity.ultimate_children_relations:
        ultimate_count = len(entity.ultimate_children_relations)
        relationships.append(f"[cyan]Ultimate Subsidiaries:[/cyan] {ultimate_count} entities")
    
    return "\n".join(relationships) if relationships else "No corporate relationships available"


def _format_related_instruments(instruments):
    """Format related instruments"""
    if not instruments:
        return "No related instruments"
    
    instrument_count = len(instruments)
    details = [f"[cyan]Total Instruments:[/cyan] {instrument_count}"]
    
    # Group by type
    by_type = {}
    for inst in instruments:
        inst_type = inst.instrument_type or "unknown"
        by_type[inst_type] = by_type.get(inst_type, 0) + 1
    
    for inst_type, count in sorted(by_type.items()):
        details.append(f"  [cyan]{inst_type.title()}:[/cyan] {count}")
    
    return "\n".join(details)
