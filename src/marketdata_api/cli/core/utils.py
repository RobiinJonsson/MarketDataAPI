"""
Shared CLI utilities, console setup, and helper functions.
"""
import os
import sys
from pathlib import Path
from typing import Any, Callable

import click
from rich import print as rprint
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Initialize Rich console for beautiful output
console = Console()

# Add project root to Python path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


def check_database_initialized() -> bool:
    """Check if database exists and offer to initialize it if not."""
    try:
        from marketdata_api.config import SQLITE_DB_PATH
        from marketdata_api.database.initialize_db import database_exists, init_database
        
        if not database_exists():
            console.print("\n[bold red]⚠️  Database not found![/bold red]")
            console.print(f"[dim]Expected location: {SQLITE_DB_PATH}[/dim]")
            console.print(
                "\n[yellow]The database needs to be initialized before using CLI commands.[/yellow]"
            )

            if click.confirm("Would you like to initialize a new database now?"):
                console.print("[cyan]Initializing database...[/cyan]")
                if init_database():
                    console.print("[green]✓ Database initialized successfully![/green]\n")
                    return True
                else:
                    console.print("[red]✗ Database initialization failed![/red]")
                    console.print(
                        "[dim]Run 'marketdata init --force' to try manual initialization.[/dim]"
                    )
                    return False
            else:
                console.print(
                    "\n[dim]To initialize manually, run: [bold]marketdata init[/bold][/dim]"
                )
                console.print(
                    "[dim]Or set custom database path with: [bold]SQLITE_DB_PATH=/path/to/db[/bold][/dim]"
                )
                return False
        return True
    except Exception as e:
        console.print(f"[red]Database check failed: {e}[/red]")
        return False


def handle_database_error(func: Callable) -> Callable:
    """Decorator to handle database connection errors gracefully."""
    import functools

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from sqlalchemy.exc import OperationalError
            
            if isinstance(e, OperationalError) and "no such table" in str(e).lower():
                console.print(f"\n[red]Database Error:[/red] {str(e)}")
                console.print(
                    "[yellow]The database appears to be missing tables. Try running:[/yellow]"
                )
                console.print("[cyan]marketdata init --force[/cyan]")
                console.print(
                    "[dim]This will recreate the database with all required tables.[/dim]"
                )
            else:
                console.print(f"[red]Error:[/red] {str(e)}")
                
            return None

    return wrapper


class CustomGroup(click.Group):
    """Custom Click group with improved help formatting."""

    def format_help(self, ctx, formatter):
        console.print(
            Panel(
                "[bold cyan]MarketDataAPI Professional CLI[/bold cyan]\n"
                "Command-line interface for financial market data operations",
                title="Welcome",
            )
        )
        super().format_help(ctx, formatter)


def format_table_output(data: list, title: str = None, max_width: int = None) -> Table:
    """Create a formatted Rich table from data."""
    if not data:
        return Table(title=title or "No Data")
    
    table = Table(title=title)
    
    # Add columns based on first row keys
    first_row = data[0]
    if isinstance(first_row, dict):
        for key in first_row.keys():
            table.add_column(str(key).title(), style="cyan")
        
        # Add rows
        for row in data:
            table.add_row(*[str(row.get(key, "")) for key in first_row.keys()])
    
    return table


def print_success(message: str):
    """Print a success message with consistent formatting."""
    console.print(f"[green]✓ {message}[/green]")


def print_error(message: str):
    """Print an error message with consistent formatting."""
    console.print(f"[red]✗ {message}[/red]")


def print_warning(message: str):
    """Print a warning message with consistent formatting."""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def print_info(message: str):
    """Print an info message with consistent formatting."""
    console.print(f"[cyan]ℹ️  {message}[/cyan]")