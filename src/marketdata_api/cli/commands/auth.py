"""Authentication CLI commands for user management"""

import logging
from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from ...config import DatabaseConfig
from ...services.core.auth_service import auth_service

console = Console()
logger = logging.getLogger(__name__)


@click.group()
def auth():
    """Authentication and user management commands"""
    pass


@auth.command()
@click.option('--username', '-u', required=True, help='Username for the new user')
@click.option('--email', '-e', required=True, help='Email address for the new user')
@click.option('--password', '-p', help='Password (will prompt if not provided)')
@click.option('--role', '-r', default='user', type=click.Choice(['user', 'admin']), 
              help='Role for the new user (default: user)')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
def create_user(username: str, email: str, password: Optional[str], role: str, force: bool):
    """Create a new user account"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        console.print("💡 Authentication is disabled for SQLite development mode", style="yellow")
        return
    
    try:
        # Prompt for password if not provided
        if not password:
            password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
        
        # Validate password length
        if len(password) < 8:
            console.print("❌ Password must be at least 8 characters long", style="bold red")
            return
        
        # Show confirmation unless force flag is used
        if not force:
            console.print(f"\n📋 Creating new user:")
            console.print(f"   Username: {username}")
            console.print(f"   Email: {email}")
            console.print(f"   Role: {role}")
            
            if not click.confirm('\nProceed with user creation?'):
                console.print("Operation cancelled", style="yellow")
                return
        
        # Create the user
        user_data = auth_service.create_user(username, email, password, [role])
        
        console.print(f"✅ User '{username}' created successfully!", style="bold green")
        console.print(f"   ID: {user_data['id']}")
        console.print(f"   Email: {user_data['email']}")
        console.print(f"   Roles: {', '.join(user_data['roles'])}")
        console.print(f"   Created: {user_data['created_at']}")
        
    except ValueError as e:
        console.print(f"❌ User creation failed: {e}", style="bold red")
    except Exception as e:
        logger.error(f"Unexpected error creating user: {e}")
        console.print(f"❌ Unexpected error: {e}", style="bold red")


@auth.command()
@click.option('--username', '-u', help='Filter by username')
@click.option('--limit', '-l', default=50, help='Maximum number of users to display')
def list_users(username: Optional[str], limit: int):
    """List all users"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        return
    
    try:
        # Get users list
        result = auth_service.list_users(limit=limit)
        users = result['users']
        total = result['total']
        
        if not users:
            console.print("📝 No users found", style="yellow")
            return
        
        # Filter by username if specified
        if username:
            users = [u for u in users if username.lower() in u['username'].lower()]
        
        # Create table
        table = Table(title=f"👥 Users ({len(users)} of {total})")
        table.add_column("Username", style="cyan")
        table.add_column("Email", style="blue")
        table.add_column("Roles", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Last Login", style="magenta")
        
        for user in users:
            status = "✅ Active" if user['is_active'] else "❌ Inactive"
            last_login = user['last_login'] or "Never"
            roles = ', '.join(user['roles'])
            
            table.add_row(
                user['username'],
                user['email'],
                roles,
                status,
                last_login
            )
        
        console.print(table)
        
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        console.print(f"❌ Error listing users: {e}", style="bold red")


@auth.command()
@click.option('--username', '-u', required=True, help='Username to modify')
@click.option('--role', '-r', required=True, type=click.Choice(['user', 'admin']), 
              help='Role to assign')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
def assign_role(username: str, role: str, force: bool):
    """Assign a role to a user"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        return
    
    try:
        # Get user first
        user = auth_service.get_user_by_username(username)
        if not user:
            console.print(f"❌ User '{username}' not found", style="bold red")
            return
        
        # Show confirmation unless force flag is used
        if not force:
            current_roles = ', '.join(user['roles'])
            console.print(f"\n📋 Assigning role to user:")
            console.print(f"   Username: {username}")
            console.print(f"   Current roles: {current_roles}")
            console.print(f"   New role: {role}")
            
            if not click.confirm('\nProceed with role assignment?'):
                console.print("Operation cancelled", style="yellow")
                return
        
        # Assign the role
        success = auth_service.assign_role_to_user(user['id'], role)
        
        if success:
            console.print(f"✅ Role '{role}' assigned to user '{username}'", style="bold green")
        else:
            console.print(f"❌ Failed to assign role '{role}' to user '{username}'", style="bold red")
        
    except Exception as e:
        logger.error(f"Error assigning role: {e}")
        console.print(f"❌ Error assigning role: {e}", style="bold red")


@auth.command()
@click.option('--username', '-u', required=True, help='Username to deactivate')
@click.option('--force', is_flag=True, help='Skip confirmation prompts')
def deactivate_user(username: str, force: bool):
    """Deactivate a user account"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        return
    
    try:
        # Get user first
        user = auth_service.get_user_by_username(username)
        if not user:
            console.print(f"❌ User '{username}' not found", style="bold red")
            return
        
        if not user['is_active']:
            console.print(f"⚠️  User '{username}' is already inactive", style="yellow")
            return
        
        # Show confirmation unless force flag is used
        if not force:
            console.print(f"\n⚠️  Deactivating user account:")
            console.print(f"   Username: {username}")
            console.print(f"   Email: {user['email']}")
            console.print(f"   This will prevent the user from logging in")
            
            if not click.confirm('\nProceed with deactivation?'):
                console.print("Operation cancelled", style="yellow")
                return
        
        # Deactivate the user
        success = auth_service.deactivate_user(user['id'])
        
        if success:
            console.print(f"✅ User '{username}' has been deactivated", style="bold green")
        else:
            console.print(f"❌ Failed to deactivate user '{username}'", style="bold red")
        
    except Exception as e:
        logger.error(f"Error deactivating user: {e}")
        console.print(f"❌ Error deactivating user: {e}", style="bold red")


@auth.command()
def setup_roles():
    """Create default roles (user and admin) if they don't exist"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        return
    
    try:
        success = auth_service.create_default_roles()
        
        if success:
            console.print("✅ Default roles created successfully", style="bold green")
            
            # Show available roles
            roles = auth_service.get_roles()
            if roles:
                table = Table(title="📋 Available Roles")
                table.add_column("Name", style="cyan")
                table.add_column("Display Name", style="blue")
                table.add_column("Description", style="green")
                table.add_column("Permissions", style="yellow")
                
                for role in roles:
                    permissions = ', '.join(role['permissions'][:3]) + \
                                (f" (+{len(role['permissions'])-3} more)" if len(role['permissions']) > 3 else "")
                    
                    table.add_row(
                        role['name'],
                        role['display_name'],
                        role['description'][:50] + "..." if len(role['description']) > 50 else role['description'],
                        permissions
                    )
                
                console.print(table)
        else:
            console.print("❌ Failed to create default roles", style="bold red")
        
    except Exception as e:
        logger.error(f"Error setting up roles: {e}")
        console.print(f"❌ Error setting up roles: {e}", style="bold red")


@auth.command()
def status():
    """Show authentication system status"""
    
    console.print("🔐 Authentication System Status\n")
    
    # Check database type
    db_type = DatabaseConfig.get_database_type()
    console.print(f"Database Type: {db_type.upper()}")
    
    # Check if authentication is enabled
    auth_enabled = auth_service.is_authentication_enabled()
    
    if auth_enabled:
        console.print("Authentication: ✅ Enabled (Production Mode)", style="bold green")
        
        try:
            # Get user and role statistics
            result = auth_service.list_users(limit=1000)
            total_users = result['total']
            active_users = len([u for u in result['users'] if u['is_active']])
            
            roles = auth_service.get_roles()
            
            console.print(f"Total Users: {total_users}")
            console.print(f"Active Users: {active_users}")
            console.print(f"Available Roles: {len(roles)}")
            
            if roles:
                console.print("\nRoles:")
                for role in roles:
                    user_count = role.get('user_count', 0)
                    console.print(f"  • {role['display_name']} ({user_count} users)")
            
        except Exception as e:
            console.print(f"⚠️  Could not retrieve user statistics: {e}", style="yellow")
    else:
        console.print("Authentication: ❌ Disabled (Development Mode)", style="yellow")
        console.print("💡 Authentication is only available with SQL Server database", style="blue")


@auth.command()  
@click.option('--admin-username', '-au', default='admin', help='Admin username (default: admin)')
@click.option('--admin-email', '-ae', default='admin@marketdata.local', help='Admin email')
@click.option('--admin-password', '-ap', help='Admin password (will prompt if not provided)')
def init():
    """Initialize authentication system with default roles and admin user"""
    
    # Check if authentication is enabled
    if not auth_service.is_authentication_enabled():
        console.print("❌ Authentication is only available in production (SQL Server) mode", style="bold red")
        console.print("💡 Switch to SQL Server database to enable authentication", style="blue")
        return
    
    try:
        console.print("🔐 Initializing Authentication System\n")
        
        # Step 1: Create default roles
        console.print("1️⃣  Creating default roles...")
        success = auth_service.create_default_roles()
        
        if success:
            console.print("   ✅ Default roles created", style="green")
        else:
            console.print("   ℹ️  Default roles already exist", style="blue")
        
        # Step 2: Check if admin user exists
        console.print(f"2️⃣  Checking for admin user '{admin_username}'...")
        existing_admin = auth_service.get_user_by_username(admin_username)
        
        if existing_admin:
            console.print(f"   ℹ️  Admin user '{admin_username}' already exists", style="blue")
            console.print("   🔐 Authentication system is ready!")
            return
        
        # Step 3: Create admin user
        console.print(f"3️⃣  Creating admin user '{admin_username}'...")
        
        # Get password
        if not admin_password:
            admin_password = click.prompt('Admin password', hide_input=True, confirmation_prompt=True)
        
        # Validate password
        if len(admin_password) < 8:
            console.print("❌ Password must be at least 8 characters long", style="bold red")
            return
        
        # Create admin user
        user_data = auth_service.create_user(admin_username, admin_email, admin_password, ['admin'])
        
        console.print(f"   ✅ Admin user created successfully", style="bold green")
        console.print(f"\n🎉 Authentication system initialized!")
        console.print(f"   Admin Username: {admin_username}")
        console.print(f"   Admin Email: {admin_email}")
        console.print(f"   User ID: {user_data['id']}")
        
    except ValueError as e:
        console.print(f"❌ Initialization failed: {e}", style="bold red")
    except Exception as e:
        logger.error(f"Unexpected error during initialization: {e}")
        console.print(f"❌ Unexpected error: {e}", style="bold red")