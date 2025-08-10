import requests
import logging
from datetime import datetime, UTC
from ..models.sqlite.legal_entity import EntityRelationship, EntityRelationshipException
from .api_utils import retry_with_backoff, log_api_call, ApiError, RetryExhaustedError

# Set up logger
logger = logging.getLogger(__name__)

GLEIF_BASE_URL = "https://api.gleif.org/api/v1/lei-records"
DEFAULT_TIMEOUT = (5, 30)  # (connect timeout, read timeout) in seconds

def _create_or_update_child_entity(session, child_data):
    """
    Create or update a child entity from GLEIF child data.
    
    Args:
        session: SQLAlchemy database session
        child_data: Child entity data from GLEIF API response
    """
    from ..database.model_mapper import map_lei_record
    from ..models.sqlite.legal_entity import LegalEntity, EntityAddress, EntityRegistration
    
    try:
        # Map the GLEIF data to our entity format
        mapped_data = map_lei_record({"data": child_data})
        entity_data = mapped_data["lei_record"]
        lei = entity_data["lei"]
        
        # Check if entity already exists
        entity = session.query(LegalEntity).filter(LegalEntity.lei == lei).first()
        if not entity:
            # Create new entity
            entity = LegalEntity(**entity_data)
            session.add(entity)
            logger.debug(f"Created new child entity: {lei}")
        else:
            # Update existing entity
            for key, value in entity_data.items():
                setattr(entity, key, value)
            logger.debug(f"Updated existing child entity: {lei}")
        
        # Update addresses if provided
        if mapped_data.get("addresses"):
            # Clear existing addresses and add new ones
            entity.addresses = []
            for addr_data in mapped_data["addresses"]:
                address = EntityAddress(**addr_data)
                entity.addresses.append(address)
        
        # Update registration if provided
        if mapped_data.get("registration"):
            if not entity.registration:
                entity.registration = EntityRegistration(**mapped_data["registration"])
            else:
                # Update existing registration
                for key, value in mapped_data["registration"].items():
                    setattr(entity.registration, key, value)
        
        return entity
        
    except Exception as e:
        logger.error(f"Error creating/updating child entity from GLEIF data: {e}", exc_info=True)
        raise

@log_api_call
@retry_with_backoff(max_retries=3, initial_backoff=2)
def fetch_lei_info(lei_code):
    """Fetches issuer info for a given LEI code from the GLEIF API."""
    url = f"{GLEIF_BASE_URL}/{lei_code}"
    try:
        logger.debug(f"Calling GLEIF API for LEI info: {lei_code}")
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data from GLEIF API: {e}", exc_info=True)
        return {"error": f"Failed to retrieve LEI information: {str(e)}"}

@log_api_call
@retry_with_backoff(max_retries=3, initial_backoff=2)
def fetch_direct_parent(lei_code):
    """Fetches direct parent information for a given LEI code."""
    # First, check if there's a direct parent relationship
    url = f"{GLEIF_BASE_URL}/{lei_code}/direct-parent"
    try:
        logger.debug(f"Calling GLEIF API for direct parent: {lei_code}")
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            # Direct parent data available
            return response.json()
        elif response.status_code == 404:
            # Check for reporting exception
            logger.debug(f"No direct parent found for {lei_code}, checking for exception")
            exception_url = f"{GLEIF_BASE_URL}/{lei_code}/direct-parent-reporting-exception"
            
            try:
                exception_response = requests.get(exception_url, timeout=DEFAULT_TIMEOUT)
                if exception_response.status_code == 200:
                    return exception_response.json()
                else:
                    logger.warning(f"No direct parent or exception found for {lei_code}")
                    return {"error": f"No direct parent or exception found for {lei_code}"}
            except requests.RequestException as ex:
                logger.error(f"Error fetching direct parent exception data: {ex}", exc_info=True)
                return {"error": f"Failed to retrieve direct parent exception information: {str(ex)}"}
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching direct parent data from GLEIF API: {e}", exc_info=True)
        return {"error": f"Failed to retrieve direct parent information: {str(e)}"}

@log_api_call
@retry_with_backoff(max_retries=3, initial_backoff=2)
def fetch_ultimate_parent(lei_code):
    """Fetches ultimate parent information for a given LEI code."""
    # First, check if there's an ultimate parent relationship
    url = f"{GLEIF_BASE_URL}/{lei_code}/ultimate-parent"
    try:
        logger.debug(f"Calling GLEIF API for ultimate parent: {lei_code}")
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            # Ultimate parent data available
            return response.json()
        elif response.status_code == 404:
            # Check for reporting exception
            logger.debug(f"No ultimate parent found for {lei_code}, checking for exception")
            exception_url = f"{GLEIF_BASE_URL}/{lei_code}/ultimate-parent-reporting-exception"
            
            try:
                exception_response = requests.get(exception_url, timeout=DEFAULT_TIMEOUT)
                if exception_response.status_code == 200:
                    return exception_response.json()
                else:
                    logger.warning(f"No ultimate parent or exception found for {lei_code}")
                    return {"error": f"No ultimate parent or exception found for {lei_code}"}
            except requests.RequestException as ex:
                logger.error(f"Error fetching ultimate parent exception data: {ex}", exc_info=True)
                return {"error": f"Failed to retrieve ultimate parent exception information: {str(ex)}"}
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching ultimate parent data from GLEIF API: {e}", exc_info=True)
        return {"error": f"Failed to retrieve ultimate parent information: {str(e)}"}

@log_api_call
@retry_with_backoff(max_retries=3, initial_backoff=2)
def fetch_direct_children(lei_code):
    """Fetches direct children information for a given LEI code."""
    # For children, we also need to handle relationship records
    url = f"{GLEIF_BASE_URL}/{lei_code}/direct-children"
    try:
        logger.debug(f"Calling GLEIF API for direct children: {lei_code}")
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Check for relationship records
            logger.debug(f"No direct children found for {lei_code}, checking relationships")
            rel_url = f"{GLEIF_BASE_URL}/{lei_code}/direct-child-relationships"
            try:
                rel_response = requests.get(rel_url, timeout=DEFAULT_TIMEOUT)
                if rel_response.status_code == 200:
                    return rel_response.json()
                else:
                    logger.info(f"No direct children relationships found for {lei_code}")
                    return {"error": f"No direct children found for {lei_code}"}
            except requests.RequestException as rel_e:
                logger.error(f"Error fetching direct child relationships: {rel_e}", exc_info=True)
                return {"error": f"Failed to retrieve direct child relationships: {str(rel_e)}"}
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching direct children data from GLEIF API: {e}", exc_info=True)
        return {"error": f"Failed to retrieve direct children information: {str(e)}"}

@log_api_call
@retry_with_backoff(max_retries=3, initial_backoff=2)
def fetch_ultimate_children(lei_code):
    """Fetches ultimate children information for a given LEI code."""
    # For children, we also need to handle relationship records
    url = f"{GLEIF_BASE_URL}/{lei_code}/ultimate-children"
    try:
        logger.debug(f"Calling GLEIF API for ultimate children: {lei_code}")
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            # Check for relationship records
            logger.debug(f"No ultimate children found for {lei_code}, checking relationships")
            rel_url = f"{GLEIF_BASE_URL}/{lei_code}/ultimate-child-relationships"
            try:
                rel_response = requests.get(rel_url, timeout=DEFAULT_TIMEOUT)
                if rel_response.status_code == 200:
                    return rel_response.json()
                else:
                    logger.info(f"No ultimate children relationships found for {lei_code}")
                    return {"error": f"No ultimate children found for {lei_code}"}
            except requests.RequestException as rel_e:
                logger.error(f"Error fetching ultimate child relationships: {rel_e}", exc_info=True)
                return {"error": f"Failed to retrieve ultimate child relationships: {str(rel_e)}"}
        else:
            response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching ultimate children data from GLEIF API: {e}", exc_info=True)
        return {"error": f"Failed to retrieve ultimate children information: {str(e)}"}

def process_parent_relationship(session, lei_code, parent_data, relationship_type):
    """
    Process parent relationship data from GLEIF API and update the database.
    
    Args:
        session: SQLAlchemy database session
        lei_code: LEI code of the child entity
        parent_data: Response data from GLEIF API for parent relationship
        relationship_type: Either 'DIRECT' or 'ULTIMATE'
    
    Returns:
        A dict with results of the operation
    """
    # Check if we received an error
    if "error" in parent_data:
        return {"error": parent_data["error"]}
    
    # Check if the response contains relationship data or exception data
    if "data" in parent_data and parent_data["data"].get("type") == "lei-records":
        # This is a parent entity record
        parent_lei = parent_data["data"]["id"]
        
        try:
            # First, create or update the parent entity from GLEIF data
            _create_or_update_child_entity(session, parent_data["data"])
            
            # Check if relationship already exists
            existing_rel = session.query(EntityRelationship).filter_by(
                parent_lei=parent_lei, 
                child_lei=lei_code,
                relationship_type=relationship_type
            ).first()
            
            if existing_rel:
                # Update existing relationship
                existing_rel.last_updated = datetime.now(UTC)
                return {"message": f"Updated existing {relationship_type.lower()} parent relationship"}
            else:
                # Create new relationship
                new_rel = EntityRelationship(
                    parent_lei=parent_lei,
                    child_lei=lei_code,
                    relationship_type=relationship_type,
                    relationship_status="ACTIVE",
                    relationship_period_start=datetime.now(UTC),
                    last_updated=datetime.now(UTC)
                )
                session.add(new_rel)
                session.flush()  # Parent relationships are few, so we flush immediately
                return {"message": f"Created new {relationship_type.lower()} parent relationship", "parent_lei": parent_lei}
        except Exception as e:
            logger.error(f"Error processing parent entity {parent_lei}: {e}", exc_info=True)
            return {"error": f"Failed to process parent entity: {str(e)}"}
    elif "data" in parent_data and parent_data["data"].get("type") == "reporting-exceptions":
        # This is a reporting exception
        exception_data = parent_data["data"]
        
        # Map the exception type
        exception_type = "DIRECT_PARENT" if relationship_type == "DIRECT" else "ULTIMATE_PARENT"
        
        # Check if exception already exists
        existing_exception = session.query(EntityRelationshipException).filter_by(
            lei=lei_code,
            exception_type=exception_type
        ).first()
        
        if existing_exception:
            # Update existing exception
            existing_exception.exception_reason = exception_data["attributes"]["reason"]
            existing_exception.exception_category = exception_data["attributes"]["category"]
            existing_exception.last_updated = datetime.now(UTC)
            
            return {"message": f"Updated existing {exception_type.lower()} exception"}
        else:
            # Create new exception
            new_exception = EntityRelationshipException(
                lei=lei_code,
                exception_type=exception_type,
                exception_reason=exception_data["attributes"]["reason"],
                exception_category=exception_data["attributes"]["category"],
                last_updated=datetime.now(UTC)
            )
            
            # Add parent information if available (if exists in the response)
            if exception_data["attributes"].get("parentEntity"):
                parent_entity = exception_data["attributes"]["parentEntity"]
                if parent_entity.get("lei"):
                    new_exception.provided_parent_lei = parent_entity["lei"]
                if parent_entity.get("name"):
                    new_exception.provided_parent_name = parent_entity["name"]
            
            session.add(new_exception)
            session.flush()
            return {"message": f"Created new {exception_type.lower()} exception"}
    
    return {"error": "Unrecognized response format from GLEIF API"}

def process_children_relationships(session, parent_lei, children_data, relationship_type, batch_size=100):
    """
    Process children relationship data from GLEIF API and update the database.
    Uses batch processing to reduce database load for entities with many children.
    
    Args:
        session: SQLAlchemy database session
        parent_lei: LEI code of the parent entity
        children_data: Response data from GLEIF API for children relationships
        relationship_type: Either 'DIRECT' or 'ULTIMATE'
        batch_size: Number of operations to batch together before flushing (default: 100)
    
    Returns:
        A dict with results of the operation
    """
    results = {"processed": 0, "errors": 0, "pruned": 0, "details": [], "batches": 0}
    
    # Check if we received an error
    if "error" in children_data:
        return {"error": children_data["error"]}
    
    # Check if we have data
    if "data" not in children_data:
        return {"error": "No data found in response"}
    
    # Get all current children relationships for this parent
    current_relationships = session.query(EntityRelationship).filter_by(
        parent_lei=parent_lei, 
        relationship_type=relationship_type
    ).all()
    
    # Create a set of existing child LEIs for faster lookups
    existing_child_leis = set()
    current_rel_map = {}
    for rel in current_relationships:
        existing_child_leis.add(rel.child_lei)
        current_rel_map[rel.child_lei] = rel
        
    # Track LEIs found in the API response
    found_child_leis = set()
    
    # Counters for batch operations
    batch_counter = 0
    
    # Process each child entity
    for child in children_data["data"]:
        if child.get("type") == "lei-records":
            child_lei = child["id"]
            found_child_leis.add(child_lei)
            
            try:
                # First, create or update the child entity from GLEIF data
                _create_or_update_child_entity(session, child)
                
                # Check if relationship already exists
                if child_lei in existing_child_leis:
                    # Update existing relationship
                    existing_rel = current_rel_map[child_lei]
                    existing_rel.last_updated = datetime.now(UTC)
                    results["processed"] += 1
                    results["details"].append({
                        "child_lei": child_lei,
                        "action": "updated"
                    })
                else:
                    # Create new relationship
                    new_rel = EntityRelationship(
                        parent_lei=parent_lei,
                        child_lei=child_lei,
                        relationship_type=relationship_type,
                        relationship_status="ACTIVE",
                        relationship_period_start=datetime.now(UTC),
                        last_updated=datetime.now(UTC)
                    )
                    session.add(new_rel)
                    results["processed"] += 1
                    results["details"].append({
                        "child_lei": child_lei,
                        "action": "created"
                    })
                    
                    # Increment batch counter
                    batch_counter += 1
                    
                    # Flush when batch size is reached
                    if batch_counter >= batch_size:
                        session.flush()
                        results["batches"] += 1
                        batch_counter = 0
                        
            except Exception as e:
                results["errors"] += 1
                results["details"].append({
                    "child_lei": child_lei,
                    "error": str(e)
                })
    
    # Flush any remaining items in the last batch
    if batch_counter > 0:
        session.flush()
        results["batches"] += 1
    
    # Batch processing for pruning
    batch_counter = 0
    
    # Prune relationships that no longer exist
    relationships_to_prune = existing_child_leis - found_child_leis
    if relationships_to_prune:
        for child_lei in relationships_to_prune:
            try:
                # Get the relationship to prune
                rel_to_prune = current_rel_map[child_lei]
                
                # Instead of deleting, mark it as inactive with an end date
                rel_to_prune.relationship_status = "INACTIVE"
                rel_to_prune.relationship_period_end = datetime.now(UTC)
                rel_to_prune.last_updated = datetime.now(UTC)
                
                results["pruned"] += 1
                results["details"].append({
                    "child_lei": child_lei,
                    "action": "pruned"
                })
                
                # Increment batch counter
                batch_counter += 1
                
                # Flush when batch size is reached
                if batch_counter >= batch_size:
                    session.flush()
                    results["batches"] += 1
                    batch_counter = 0
                    
            except Exception as e:
                results["errors"] += 1
                results["details"].append({
                    "child_lei": child_lei,
                    "action": "prune_failed",
                    "error": str(e)
                })
        
        # Flush any remaining pruned items in the last batch
        if batch_counter > 0:
            session.flush()
            results["batches"] += 1
    
    return results

def prune_parent_relationship(session, lei_code, relationship_type):
    """
    Prune any parent relationships of the specified type that are no longer valid.
    This is used when a relationship previously existed but is now replaced by an exception.
    
    Args:
        session: SQLAlchemy database session
        lei_code: LEI code of the child entity
        relationship_type: Either 'DIRECT' or 'ULTIMATE'
        
    Returns:
        bool: True if a relationship was pruned, False otherwise
    """
    # Find existing parent relationship of this type
    existing_rel = session.query(EntityRelationship).filter_by(
        child_lei=lei_code,
        relationship_type=relationship_type
    ).first()
    
    if existing_rel:
        # Mark as inactive instead of deleting
        existing_rel.relationship_status = "INACTIVE"
        existing_rel.relationship_period_end = datetime.now(UTC)
        existing_rel.last_updated = datetime.now(UTC)
        return True
    
    return False

def sync_entity_relationships(session, lei_code, batch_size=100):
    """
    Synchronize parent and direct child relationships for an entity from GLEIF API.
    Optimized to only fetch direct parent, ultimate parent, and direct children
    to avoid database bloat from extensive ultimate children structures.
    
    Args:
        session: SQLAlchemy database session
        lei_code: LEI code of the entity to synchronize
        batch_size: Number of operations to batch together before flushing (default: 100)
    
    Returns:
        A dict with results of the operation
    """
    results = {
        "direct_parent": None,
        "ultimate_parent": None,
        "direct_children": None,
        "ultimate_children": "skipped"  # Indicate that this was intentionally skipped
    }
    
    # Process direct parent
    direct_parent_data = fetch_direct_parent(lei_code)
    results["direct_parent"] = process_parent_relationship(
        session, lei_code, direct_parent_data, "DIRECT"
    )
    
    # Check if we need to prune a direct parent relationship
    if (results["direct_parent"].get("message") and 
        "exception" in results["direct_parent"]["message"] and
        prune_parent_relationship(session, lei_code, "DIRECT")):
        # If the current result is an exception but a relationship existed before
        results["direct_parent"]["pruned_relationship"] = True
    
    # Process ultimate parent
    ultimate_parent_data = fetch_ultimate_parent(lei_code)
    results["ultimate_parent"] = process_parent_relationship(
        session, lei_code, ultimate_parent_data, "ULTIMATE"
    )
    
    # Check if we need to prune an ultimate parent relationship
    if (results["ultimate_parent"].get("message") and 
        "exception" in results["ultimate_parent"]["message"] and
        prune_parent_relationship(session, lei_code, "ULTIMATE")):
        # If the current result is an exception but a relationship existed before
        results["ultimate_parent"]["pruned_relationship"] = True
    
    # Process direct children only (skip ultimate children to avoid database bloat)
    direct_children_data = fetch_direct_children(lei_code)
    results["direct_children"] = process_children_relationships(
        session, lei_code, direct_children_data, "DIRECT", batch_size
    )
    
    # Skip ultimate children processing to avoid database bloat
    # Ultimate children can be extensive and are often not needed for most use cases
    
    return results

