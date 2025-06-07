"""
Convenience script for updating documentation after API changes
"""

import subprocess
import sys
from pathlib import Path

def run_generation():
    """Run the documentation generation script"""
    script_path = Path(__file__).parent / 'generate_docs.py'
    
    try:
        print("🔄 Updating API documentation...")
        result = subprocess.run([sys.executable, str(script_path)], 
                              capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
            
        if result.returncode == 0:
            print("\n✅ Documentation update completed successfully!")
            print("\nNext steps:")
            print("1. Review generated files in docs/openapi/ and docs/postman/")
            print("2. Test the API documentation at /api/v1/swagger")
            print("3. Commit the updated documentation files")
        else:
            print(f"\n❌ Documentation update failed with exit code {result.returncode}")
            
    except Exception as e:
        print(f"❌ Error running documentation generation: {e}")

if __name__ == "__main__":
    run_generation()
