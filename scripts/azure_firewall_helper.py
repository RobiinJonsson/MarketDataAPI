#!/usr/bin/env python3
"""
Azure SQL Firewall Helper

This script helps you manage Azure SQL firewall rules to allow access
from your current IP address.
"""

import os
import sys
import requests
import logging
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_current_ip():
    """Get current public IP address"""
    try:
        # Try multiple services for reliability
        services = [
            'https://api.ipify.org',
            'https://httpbin.org/ip',
            'https://icanhazip.com'
        ]
        
        for service in services:
            try:
                if service == 'https://httpbin.org/ip':
                    response = requests.get(service, timeout=5)
                    return response.json()['origin']
                elif service == 'https://icanhazip.com':
                    response = requests.get(service, timeout=5)
                    return response.text.strip()
                else:
                    response = requests.get(service, timeout=5)
                    return response.text.strip()
            except:
                continue
        
        return None
        
    except Exception as e:
        logger.error(f"Failed to get current IP: {e}")
        return None

def show_firewall_instructions():
    """Show instructions for adding firewall rule"""
    current_ip = get_current_ip()
    
    print("🔥 Azure SQL Firewall Configuration")
    print("=" * 50)
    
    if current_ip:
        logger.info(f"Your current public IP: {current_ip}")
    else:
        logger.warning("Could not detect your current IP automatically")
        current_ip = "YOUR_IP_ADDRESS"
    
    print("\n📋 How to add firewall rule:")
    print("\nOption 1: Using Azure Portal")
    print("1. Go to https://portal.azure.com")
    print("2. Navigate to your SQL Server: myfreesqlmddbserver01")
    print("3. Go to 'Networking' or 'Firewalls and virtual networks'")
    print("4. Add a new rule:")
    print(f"   - Rule name: DevAccess")
    print(f"   - Start IP: {current_ip}")
    print(f"   - End IP: {current_ip}")
    print("5. Click 'Save'")
    print("6. Wait 5 minutes for changes to take effect")
    
    print("\nOption 2: Using Azure CLI")
    print("If you have Azure CLI installed:")
    print(f"az sql server firewall-rule create \\")
    print(f"  --resource-group your-resource-group \\")
    print(f"  --server myfreesqlmddbserver01 \\")
    print(f"  --name DevAccess \\")
    print(f"  --start-ip-address {current_ip} \\")
    print(f"  --end-ip-address {current_ip}")
    
    print("\nOption 3: Allow Azure Services")
    print("For testing, you can temporarily allow all Azure services:")
    print("1. In Azure Portal, go to your SQL Server")
    print("2. Go to 'Networking'")
    print("3. Toggle 'Allow Azure services and resources to access this server'")
    print("⚠️  Note: This is less secure, use only for testing")

def test_connection_after_firewall():
    """Test connection after firewall configuration"""
    print("\n🧪 Testing connection...")
    
    try:
        from marketdata_api.database.base import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            if result.fetchone()[0] == 1:
                logger.info("✅ Database connection successful!")
                return True
            else:
                logger.error("❌ Database connection test failed")
                return False
                
    except Exception as e:
        if "Client with IP address" in str(e) and "is not allowed to access" in str(e):
            logger.error("❌ Still blocked by firewall")
            logger.error("Please check that you added the correct IP address")
            logger.error("Changes can take up to 5 minutes to take effect")
        else:
            logger.error(f"❌ Connection failed: {str(e)}")
        return False

def main():
    """Main function"""
    print("🌐 Azure SQL Firewall Helper")
    print("=" * 40)
    
    # Show current status
    try:
        from marketdata_api.config import AZURE_SQL_SERVER, AZURE_SQL_DATABASE
        logger.info(f"Server: {AZURE_SQL_SERVER}")
        logger.info(f"Database: {AZURE_SQL_DATABASE}")
    except:
        logger.warning("Could not load database configuration")
    
    print()
    
    # Test current connection
    print("Testing current connection...")
    try:
        success = test_connection_after_firewall()
        if success:
            logger.info("🎉 Connection already works! No firewall changes needed.")
            return
    except:
        pass
    
    # Show instructions
    show_firewall_instructions()
    
    print("\n" + "=" * 50)
    print("After adding the firewall rule:")
    print("1. Wait 5 minutes")
    print("2. Run this script again to test")
    print("3. Or run: python scripts/test_production_compatibility.py")

if __name__ == "__main__":
    main()
