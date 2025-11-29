"""
Legal Entity Utilities

Pure utility functions for legal entity data processing and response building.
Provides CLI-style rich data extraction for legal entities similar to instrument utilities.
"""





def build_legal_entity_response(entity, include_rich_details=True):
    """
    Build comprehensive response with CLI-style rich data extraction for legal entities.
    
    Args:
        entity: SQLAlchemy LegalEntity model instance (SQLite or SQL Server)
        include_rich_details: Whether to include rich data extraction and analysis
        
    Returns:
        dict: Comprehensive entity response with relationships, addresses, status indicators, etc.
    """
    # Both SQLite and SQL Server models now have to_api_response method
    response = entity.to_api_response(
        include_relationships=True, 
        include_addresses=True, 
        include_registration=True
    )

    if include_rich_details:
        # Add CLI-style rich data extraction
        response.update(_extract_rich_entity_status(entity))
        response.update(_extract_rich_corporate_structure(entity))
        response.update(_extract_rich_registration_details(entity))

    # Add entity counts and relationships summary
    response.update(_extract_entity_counts_and_summary(entity))

    return response


def _extract_rich_entity_status(entity):
    """Extract rich status indicators like CLI formatting"""
    status_info = {
        "status_indicators": [],
        "display_status": ""
    }
    
    # Status indicators
    status_icons = []
    
    if entity.status == "ACTIVE":
        status_icons.append("✅ Active")
    elif entity.status == "INACTIVE":
        status_icons.append("❌ Inactive")
    else:
        status_icons.append(f"⚠️ {entity.status}")
    
    if entity.bic:
        status_icons.append("🏦 BIC Available")
    
    if hasattr(entity, 'addresses') and entity.addresses:
        status_icons.append(f"🏠 {len(entity.addresses)} Address(es)")
    
    if hasattr(entity, 'instruments') and entity.instruments:
        status_icons.append(f"📊 {len(entity.instruments)} Related Instrument(s)")
    
    # Check for corporate relationships
    relationships_count = 0
    if entity.direct_parent_relation:
        relationships_count += 1
    if entity.ultimate_parent_relation:
        relationships_count += 1
    if hasattr(entity, 'direct_children_relations') and entity.direct_children_relations:
        relationships_count += len(entity.direct_children_relations)
    if hasattr(entity, 'ultimate_children_relations') and entity.ultimate_children_relations:
        relationships_count += len(entity.ultimate_children_relations)
    
    if relationships_count > 0:
        status_icons.append(f"🔗 {relationships_count} Corporate Relationship(s)")
    
    status_info["status_indicators"] = status_icons
    status_info["display_status"] = " • ".join(status_icons) if status_icons else "ℹ️ Basic Information"
    
    return status_info


def _extract_rich_corporate_structure(entity):
    """Extract corporate structure information like CLI formatting"""
    structure_info = {
        "corporate_structure": {
            "has_parent": False,
            "has_children": False,
            "parent_entities": [],
            "child_entities": [],
            "structure_summary": ""
        }
    }
    
    parent_entities = []
    child_entities = []
    
    # Direct parent
    if entity.direct_parent_relation:
        parent_entities.append({
            "type": "direct_parent",
            "lei": entity.direct_parent_relation.parent_lei,
            "name": getattr(entity.direct_parent_relation, 'parent_name', 'N/A'),
            "relationship_type": getattr(entity.direct_parent_relation, 'relationship_type', 'N/A')
        })
    
    # Ultimate parent (if different from direct)
    if (entity.ultimate_parent_relation and 
        entity.ultimate_parent_relation.parent_lei != getattr(entity.direct_parent_relation, 'parent_lei', None)):
        parent_entities.append({
            "type": "ultimate_parent",
            "lei": entity.ultimate_parent_relation.parent_lei,
            "name": getattr(entity.ultimate_parent_relation, 'parent_name', 'N/A'),
            "relationship_type": getattr(entity.ultimate_parent_relation, 'relationship_type', 'N/A')
        })
    
    # Direct children
    if hasattr(entity, 'direct_children_relations') and entity.direct_children_relations:
        for child_rel in entity.direct_children_relations:
            child_entities.append({
                "type": "direct_child",
                "lei": child_rel.child_lei,
                "name": getattr(child_rel, 'child_name', 'N/A'),
                "relationship_type": getattr(child_rel, 'relationship_type', 'N/A')
            })
    
    structure_info["corporate_structure"].update({
        "has_parent": len(parent_entities) > 0,
        "has_children": len(child_entities) > 0,
        "parent_entities": parent_entities,
        "child_entities": child_entities,
    })
    
    # Create structure summary
    summary_parts = []
    if parent_entities:
        summary_parts.append(f"{len(parent_entities)} parent(s)")
    if child_entities:
        summary_parts.append(f"{len(child_entities)} child(ren)")
    
    if summary_parts:
        structure_info["corporate_structure"]["structure_summary"] = " • ".join(summary_parts)
    else:
        structure_info["corporate_structure"]["structure_summary"] = "Standalone entity"
    
    return structure_info


def _extract_rich_registration_details(entity):
    """Extract rich registration and legal details like CLI formatting"""
    registration_info = {
        "registration_details": {
            "formatted_dates": {},
            "legal_classification": {},
            "geographical_info": {}
        }
    }
    
    # Format dates
    formatted_dates = {}
    if entity.creation_date:
        formatted_dates["creation"] = {
            "date": entity.creation_date.isoformat() if hasattr(entity.creation_date, 'isoformat') else str(entity.creation_date),
            "formatted": entity.creation_date.strftime("%Y-%m-%d") if hasattr(entity.creation_date, 'strftime') else str(entity.creation_date)
        }
    
    # Check for last update field (could be last_update or last_updated)
    last_update_field = None
    if hasattr(entity, 'last_update') and entity.last_update:
        last_update_field = entity.last_update
    elif hasattr(entity, 'last_updated') and entity.last_updated:
        last_update_field = entity.last_updated
        
    if last_update_field:
        formatted_dates["last_update"] = {
            "date": last_update_field.isoformat() if hasattr(last_update_field, 'isoformat') else str(last_update_field),
            "formatted": last_update_field.strftime("%Y-%m-%d") if hasattr(last_update_field, 'strftime') else str(last_update_field)
        }
    
    registration_info["registration_details"]["formatted_dates"] = formatted_dates
    
    # Legal classification
    legal_classification = {
        "jurisdiction_description": _get_jurisdiction_description(entity.jurisdiction),
        "legal_form_description": _get_legal_form_description(entity.legal_form),
        "registration_status": entity.status
    }
    
    registration_info["registration_details"]["legal_classification"] = legal_classification
    
    return registration_info


def _extract_entity_counts_and_summary(entity):
    """Extract entity counts and summary information"""
    counts_info = {
        "entity_counts": {
            "addresses_count": 0,
            "relationships_count": 0,
            "instruments_count": 0
        },
        "entity_summary": ""
    }
    
    # Count addresses
    if hasattr(entity, 'addresses') and entity.addresses:
        counts_info["entity_counts"]["addresses_count"] = len(entity.addresses)
    
    # Count relationships
    relationships_count = 0
    if entity.direct_parent_relation:
        relationships_count += 1
    if entity.ultimate_parent_relation:
        relationships_count += 1
    if hasattr(entity, 'direct_children_relations') and entity.direct_children_relations:
        relationships_count += len(entity.direct_children_relations)
    if hasattr(entity, 'ultimate_children_relations') and entity.ultimate_children_relations:
        relationships_count += len(entity.ultimate_children_relations)
    
    counts_info["entity_counts"]["relationships_count"] = relationships_count
    
    # Count related instruments
    if hasattr(entity, 'instruments') and entity.instruments:
        counts_info["entity_counts"]["instruments_count"] = len(entity.instruments)
    
    # Create summary
    summary_parts = []
    if counts_info["entity_counts"]["addresses_count"] > 0:
        summary_parts.append(f"{counts_info['entity_counts']['addresses_count']} addresses")
    if counts_info["entity_counts"]["relationships_count"] > 0:
        summary_parts.append(f"{counts_info['entity_counts']['relationships_count']} relationships")
    if counts_info["entity_counts"]["instruments_count"] > 0:
        summary_parts.append(f"{counts_info['entity_counts']['instruments_count']} instruments")
    
    counts_info["entity_summary"] = " • ".join(summary_parts) if summary_parts else "Basic entity information only"
    
    # Add the full relationships data from the model
    try:
        model_response = entity.to_api_response(
            include_relationships=True, include_addresses=True, include_registration=True
        )
        if 'relationships' in model_response:
            counts_info['relationships'] = model_response['relationships']
    except Exception as e:
        # If there's an error getting relationships, just continue without them
        pass
    
    return counts_info


def format_legal_entity_list_response(entities, total_count, page, per_page):
    """
    Format a list of legal entities for API response.
    
    Args:
        entities: List of LegalEntity model instances
        total_count: Total number of entities matching the query
        page: Current page number
        per_page: Items per page
        
    Returns:
        dict: Formatted response with data and metadata
    """
    return {
        "status": "success",
        "data": [build_legal_entity_response(entity) for entity in entities],
        "meta": {
            "page": page,
            "per_page": per_page,
            "total": total_count,
            "has_next": (page * per_page) < total_count,
            "has_prev": page > 1,
        },
    }


def _get_jurisdiction_description(jurisdiction_code):
    """Get human-readable description for jurisdiction code"""
    # Common jurisdiction codes - extend as needed
    jurisdiction_descriptions = {
        "US": "United States",
        "GB": "United Kingdom",
        "DE": "Germany",
        "FR": "France",
        "NL": "Netherlands",
        "SE": "Sweden",
        "CH": "Switzerland",
        "CA": "Canada",
        "AU": "Australia",
        "JP": "Japan",
        "SG": "Singapore",
        "HK": "Hong Kong",
        # Add more as needed
    }
    
    return jurisdiction_descriptions.get(jurisdiction_code, f"Jurisdiction: {jurisdiction_code}")


def _get_legal_form_description(legal_form_code):
    """Get human-readable description for legal form code"""
    # Common legal form codes - extend as needed
    legal_form_descriptions = {
        "BYQJ": "Public Limited Company",
        "W22N": "Private Limited Company",
        "XLMS": "Partnership",
        "929Q": "Limited Liability Company",
        # Add more based on your data
    }
    
    return legal_form_descriptions.get(legal_form_code, f"Legal Form: {legal_form_code}")