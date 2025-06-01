"""
Test script to demonstrate the batch processing feature of the GLEIF API integration
"""
import sys
import os
import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time
from datetime import datetime, UTC
from textwrap import dedent

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from marketdata_api.config import Config
from marketdata_api.models.legal_entity import LegalEntity, EntityRelationship
from marketdata_api.services.gleif import sync_entity_relationships

def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))

def test_batching():
    """Test relationship batch processing with different batch sizes"""
    # Create database engine and session
    engine = create_engine(f"sqlite:///{Config.DATABASE_PATH}")
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Test entities with known relationships
    # Apple Inc. (HWUPKR0MPOU8FGXBT394) - has 8 direct children, 15 ultimate children
    # Microsoft (INR2EJN1ERAN0W5ZP974) - has more children
    test_entity = "INR2EJN1ERAN0W5ZP974"  # Microsoft
    
    try:
        print(f"Testing batch processing with Microsoft (LEI: {test_entity})")
        print("\n--------------------------------------------------------")
        
        # First, test with a small batch size (1 item per batch)
        print("\n1. Testing with batch_size=1 (maximum batching):")
        print("-----------------------------------------------")
        start_time = time.time()
        results_small_batch = sync_entity_relationships(session, test_entity, batch_size=1)
        small_batch_time = time.time() - start_time
        
        direct_children_small = results_small_batch.get("direct_children", {})
        ultimate_children_small = results_small_batch.get("ultimate_children", {})
        
        print(f"Direct Children:")
        print(f"  Processed: {direct_children_small.get('processed', 'N/A')} relationship(s)")
        print(f"  Batches: {direct_children_small.get('batches', 'N/A')}")
        print(f"Ultimate Children:")
        print(f"  Processed: {ultimate_children_small.get('processed', 'N/A')} relationship(s)")
        print(f"  Batches: {ultimate_children_small.get('batches', 'N/A')}")
        print(f"Execution time: {small_batch_time:.4f} seconds")
        
        # Reset database state (rollback changes)
        session.rollback()
        
        # Now test with a large batch size (all items in one batch)
        print("\n2. Testing with batch_size=1000 (minimal batching):")
        print("--------------------------------------------------")
        start_time = time.time()
        results_large_batch = sync_entity_relationships(session, test_entity, batch_size=1000)
        large_batch_time = time.time() - start_time
        
        direct_children_large = results_large_batch.get("direct_children", {})
        ultimate_children_large = results_large_batch.get("ultimate_children", {})
        
        print(f"Direct Children:")
        print(f"  Processed: {direct_children_large.get('processed', 'N/A')} relationship(s)")
        print(f"  Batches: {direct_children_large.get('batches', 'N/A')}")
        print(f"Ultimate Children:")
        print(f"  Processed: {ultimate_children_large.get('processed', 'N/A')} relationship(s)")
        print(f"  Batches: {ultimate_children_large.get('batches', 'N/A')}")
        print(f"Execution time: {large_batch_time:.4f} seconds")
        
        # Compare results
        print("\n3. Performance Comparison:")
        print("------------------------")
        print(f"Small batch (size=1): {small_batch_time:.4f} seconds")
        print(f"Large batch (size=1000): {large_batch_time:.4f} seconds")
        
        if small_batch_time > large_batch_time:
            print(f"Large batch was {(small_batch_time/large_batch_time):.2f}x faster")
        else:
            print(f"Small batch was {(large_batch_time/small_batch_time):.2f}x faster")
        
        print("\n4. Recommended optimal batch size:")
        print("--------------------------------")
        recommendation = dedent("""
            For most cases, a batch size between 50-200 is a good balance:
            - Small enough to avoid long-running transactions
            - Large enough to reduce the overhead of frequent database flushes
            
            For entities with very large relationship trees (hundreds or thousands):
            - Consider increasing batch size to 500-1000
            - Run synchronization during off-peak hours
            
            For time-critical operations:
            - Use smaller batch sizes (10-50) to ensure more responsive UI
            - Consider implementing a background job for relationship syncing
        """)
        print(recommendation)
        
        # Rollback to not affect database
        session.rollback()
        
    except Exception as e:
        print(f"Error during batch testing: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    print("Starting batch processing test...")
    test_batching()
