"""
Test script to demonstrate the pruning feature of the GLEIF API integration
"""
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, UTC

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from marketdata_api.config import Config
from marketdata_api.models.legal_entity import LegalEntity, EntityRelationship
from marketdata_api.services.gleif import sync_entity_relationships

def test_pruning():
    """Test the relationship pruning functionality"""
    # Create database engine and session
    engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # We'll use Apple Inc. (HWUPKR0MPOU8FGXBT394) as our parent entity
        parent_lei = "HWUPKR0MPOU8FGXBT394"
        
        # Create a fake child entity just for this test
        fake_child_lei = "FAKECHILD12345678901A"
        
        # Check if the fake entity already exists, create if not
        fake_entity = session.query(LegalEntity).filter_by(lei=fake_child_lei).first()
        if not fake_entity:
            fake_entity = LegalEntity(
                lei=fake_child_lei,
                name="Fake Child Entity for Pruning Test",
                jurisdiction="TEST",
                legal_form="TEST",
                registered_as="TEST",
                status="ACTIVE",
                registration_status="ISSUED",
                managing_lou="TEST"
            )
            session.add(fake_entity)
            session.flush()
            print(f"Created fake entity: {fake_child_lei}")
        
        # Create a fake direct relationship from parent to this child
        fake_rel = EntityRelationship(
            parent_lei=parent_lei,
            child_lei=fake_child_lei,
            relationship_type="DIRECT",
            relationship_status="ACTIVE",
            relationship_period_start=datetime.now(UTC),
            last_updated=datetime.now(UTC)
        )
        session.add(fake_rel)
        
        # Create a fake ultimate relationship as well
        fake_ultimate_rel = EntityRelationship(
            parent_lei=parent_lei,
            child_lei=fake_child_lei,
            relationship_type="ULTIMATE",
            relationship_status="ACTIVE",
            relationship_period_start=datetime.now(UTC),
            last_updated=datetime.now(UTC)
        )
        session.add(fake_ultimate_rel)
        
        session.commit()
        print(f"Created fake relationships between {parent_lei} and {fake_child_lei}")
        
        # Now sync the parent entity, which should prune these fake relationships
        print("\nSyncing parent entity relationships, this should prune our fake relationships...")
        results = sync_entity_relationships(session, parent_lei)
        
        # Check pruning results
        direct_children_result = results.get("direct_children", {})
        print(f"\nDirect Children Pruning:")
        print(f"  Processed: {direct_children_result.get('processed', 'N/A')} relationship(s)")
        print(f"  Pruned: {direct_children_result.get('pruned', 'N/A')} relationship(s)")
        
        ultimate_children_result = results.get("ultimate_children", {})
        print(f"\nUltimate Children Pruning:")
        print(f"  Processed: {ultimate_children_result.get('processed', 'N/A')} relationship(s)")
        print(f"  Pruned: {ultimate_children_result.get('pruned', 'N/A')} relationship(s)")
        
        # Check if our fake relationship was pruned
        pruned_direct = session.query(EntityRelationship).filter_by(
            parent_lei=parent_lei,
            child_lei=fake_child_lei,
            relationship_type="DIRECT",
            relationship_status="INACTIVE"
        ).first()
        
        if pruned_direct:
            print(f"\nSuccess! The fake direct relationship was pruned (marked inactive).")
            print(f"  Relationship period end: {pruned_direct.relationship_period_end}")
        else:
            print("\nWarning: The fake direct relationship was not properly pruned!")
            
        # Check if our fake ultimate relationship was pruned
        pruned_ultimate = session.query(EntityRelationship).filter_by(
            parent_lei=parent_lei,
            child_lei=fake_child_lei,
            relationship_type="ULTIMATE",
            relationship_status="INACTIVE"
        ).first()
        
        if pruned_ultimate:
            print(f"Success! The fake ultimate relationship was pruned (marked inactive).")
            print(f"  Relationship period end: {pruned_ultimate.relationship_period_end}")
        else:
            print("Warning: The fake ultimate relationship was not properly pruned!")
        
        # Cleanup - remove the fake entity and its relationships
        print("\nCleaning up test data...")
        session.query(EntityRelationship).filter_by(child_lei=fake_child_lei).delete()
        session.query(EntityRelationship).filter_by(parent_lei=fake_child_lei).delete()
        session.query(LegalEntity).filter_by(lei=fake_child_lei).delete()
        session.commit()
        print("Test data cleanup complete.")
        
    except Exception as e:
        print(f"Error during pruning test: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("Starting relationship pruning test...")
    test_pruning()
