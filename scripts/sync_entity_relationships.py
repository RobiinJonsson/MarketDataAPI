"""
Utility script to demonstrate parent/child relationship synchronization
"""
import sys
import os
import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from marketdata_api.config import Config
from marketdata_api.database.base import Base
from marketdata_api.models.legal_entity import LegalEntity, EntityRelationship, EntityRelationshipException
from marketdata_api.services.gleif import sync_entity_relationships

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def sync_entity_demo(lei_code):
    """Demo function to sync entity relationships for a given LEI code"""
    # Create database engine and session
    engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # First, check if the entity exists
        entity = session.query(LegalEntity).filter_by(lei=lei_code).first()
        
        if not entity:
            print(f"Entity with LEI {lei_code} not found in the database.")
            print("Creating a placeholder entity...")
            
            # Create placeholder entity for demo purposes
            # In a real application, you would fetch full entity data from GLEIF
            entity = LegalEntity(
                lei=lei_code,
                name=f"Entity {lei_code}",
                jurisdiction="UNKNOWN",
                legal_form="UNKNOWN",
                registered_as="UNKNOWN",
                status="ACTIVE",
                registration_status="ISSUED",
                managing_lou="UNKNOWN"
            )
            session.add(entity)
            session.flush()
            print(f"Created placeholder entity with LEI {lei_code}")
        
        # Sync relationships
        print(f"\nSyncing relationships for entity with LEI {lei_code}...")
        results = sync_entity_relationships(session, lei_code)
        print("\nSync Results:")
        print_json(results)
        
        # Commit changes
        session.commit()
        
        # Display relationships after sync
        print("\nRelationships after sync:")
        
        # Direct parent
        direct_parent_rel = session.query(EntityRelationship).filter_by(
            child_lei=lei_code, relationship_type="DIRECT"
        ).first()
        
        if direct_parent_rel:
            print(f"Direct Parent: {direct_parent_rel.parent_lei}")
        else:
            # Check for exception
            direct_exception = session.query(EntityRelationshipException).filter_by(
                lei=lei_code, exception_type="DIRECT_PARENT"
            ).first()
            
            if direct_exception:
                print(f"Direct Parent Exception: {direct_exception.exception_category} - {direct_exception.exception_reason}")
                if direct_exception.provided_parent_name:
                    print(f"  Provided Parent: {direct_exception.provided_parent_name}")
            else:
                print("No direct parent relationship or exception found")
        
        # Ultimate parent
        ultimate_parent_rel = session.query(EntityRelationship).filter_by(
            child_lei=lei_code, relationship_type="ULTIMATE"
        ).first()
        
        if ultimate_parent_rel:
            print(f"Ultimate Parent: {ultimate_parent_rel.parent_lei}")
        else:
            # Check for exception
            ultimate_exception = session.query(EntityRelationshipException).filter_by(
                lei=lei_code, exception_type="ULTIMATE_PARENT"
            ).first()
            
            if ultimate_exception:
                print(f"Ultimate Parent Exception: {ultimate_exception.exception_category} - {ultimate_exception.exception_reason}")
                if ultimate_exception.provided_parent_name:
                    print(f"  Provided Parent: {ultimate_exception.provided_parent_name}")
            else:
                print("No ultimate parent relationship or exception found")
          # Direct children
        direct_children = session.query(EntityRelationship).filter_by(
            parent_lei=lei_code, relationship_type="DIRECT", relationship_status="ACTIVE"
        ).all()
        
        pruned_direct = session.query(EntityRelationship).filter_by(
            parent_lei=lei_code, relationship_type="DIRECT", relationship_status="INACTIVE"
        ).count()
        
        print(f"\nDirect Children: {len(direct_children)} active, {pruned_direct} pruned")
        for idx, child_rel in enumerate(direct_children[:10], 1):  # Show at most 10 children
            print(f"  {idx}. {child_rel.child_lei}")
        
        if len(direct_children) > 10:
            print(f"  ... and {len(direct_children) - 10} more")
          # Ultimate children
        ultimate_children = session.query(EntityRelationship).filter_by(
            parent_lei=lei_code, relationship_type="ULTIMATE", relationship_status="ACTIVE"
        ).all()
        
        pruned_ultimate = session.query(EntityRelationship).filter_by(
            parent_lei=lei_code, relationship_type="ULTIMATE", relationship_status="INACTIVE"
        ).count()
        
        print(f"\nUltimate Children: {len(ultimate_children)} active, {pruned_ultimate} pruned")
        for idx, child_rel in enumerate(ultimate_children[:10], 1):  # Show at most 10 children
            print(f"  {idx}. {child_rel.child_lei}")
        
        if len(ultimate_children) > 10:
            print(f"  ... and {len(ultimate_children) - 10} more")
        
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sync_entity_relationships.py <LEI_CODE>")
        print("Example: python sync_entity_relationships.py HWUPKR0MPOU8FGXBT394")
        sys.exit(1)
    
    lei_code = sys.argv[1]
    print(f"Starting entity relationship sync demo for LEI: {lei_code}")
    sync_entity_demo(lei_code)
