"""
MarketDataAPI Professional CLI - Modular Implementation

A command-line interface for the MarketDataAPI using Click framework
for professional-grade CLI with proper command grouping, help, and error handling.

Install with: pip install -e .
Use with: marketdata instruments list
"""
import click

import importlib.metadata

from .core.utils import CustomGroup, console
from .commands.utilities import stats, cfi, init
from .commands.instruments import instruments


def version_callback(ctx, param, value):
    """Callback to show version and exit"""
    if not value or ctx.resilient_parsing:
        return
    try:
        pkg_version = importlib.metadata.version("marketdata-api")
    except importlib.metadata.PackageNotFoundError:
        pkg_version = "unknown"
    console.print(f"[green]MarketDataAPI CLI version: {pkg_version}[/green]")
    ctx.exit()


@click.group(cls=CustomGroup, invoke_without_command=True)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output")
@click.option(
    "--format", default="table", type=click.Choice(["table", "json"]), help="Output format"
)
@click.option(
    "--version", 
    is_flag=True, 
    expose_value=False, 
    is_eager=True,
    callback=version_callback,
    help="Show version and exit"
)
@click.pass_context
def cli(ctx, verbose, format):
    """MarketDataAPI Professional CLI - Financial market data operations"""
    # Ensure ctx.obj exists for command context sharing
    ctx.ensure_object(dict)
    ctx.obj["verbose"] = verbose
    ctx.obj["format"] = format

    # Show help if no command provided
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


# Register utility commands
cli.add_command(stats)
cli.add_command(cfi)
cli.add_command(init)

# Register domain command groups
cli.add_command(instruments)

# Import and register remaining command modules
from .commands.transparency import transparency
from .commands.mic import mic
from .commands.figi import figi
from .commands.entities import entities
from .commands.files import files
from .commands.api import api

cli.add_command(transparency)
cli.add_command(mic)
cli.add_command(figi)
cli.add_command(entities)
cli.add_command(files)
cli.add_command(api)


def main():
    """Entry point for the CLI when installed as a package"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        raise


if __name__ == "__main__":
    main()