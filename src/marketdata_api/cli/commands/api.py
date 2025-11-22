"""
API Server Commands

Commands for starting and managing the Flask API server.
"""
import click
import os
from ..core.utils import console


@click.group()
def api():
    """API server management commands"""
    pass


@api.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=5000, type=int, help="Port to bind to")
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option("--reload", is_flag=True, default=True, help="Enable auto-reload on code changes (default: True)")
@click.option("--no-reload", is_flag=True, help="Disable auto-reload")
def start(host, port, debug, reload, no_reload):
    """Start the Flask API server"""
    try:
        # Handle reload options
        use_reloader = reload and not no_reload
        
        # Set Flask environment variables
        if debug:
            os.environ["FLASK_ENV"] = "development"
            os.environ["FLASK_DEBUG"] = "1"
        else:
            os.environ["FLASK_ENV"] = "production"
            os.environ["FLASK_DEBUG"] = "0"
        
        # Import and create the Flask app
        from ...import create_app
        
        console.print(f"[bold green]Starting MarketDataAPI server on {host}:{port}[/bold green]")
        if debug:
            console.print("[yellow]Debug mode enabled[/yellow]")
        if use_reloader:
            console.print("[cyan]Auto-reload enabled - server will restart on code changes[/cyan]")
        
        app = create_app()
        
        # Start the server
        app.run(
            host=host,
            port=port,
            debug=debug,
            use_reloader=use_reloader
        )
        
    except Exception as e:
        console.print(f"[red]Error starting API server: {e}[/red]")
        raise click.Abort()


@api.command()
def stop():
    """Stop running Flask API servers"""
    try:
        import psutil
        import signal
        
        stopped_count = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = proc.info.get('cmdline', [])
                if (cmdline and 
                    any('marketdata_api' in str(arg) for arg in cmdline) and
                    any('api' in str(arg) and 'start' in str(arg) for arg in cmdline)):
                    
                    console.print(f"[yellow]Stopping API server (PID: {proc.info['pid']})[/yellow]")
                    proc.terminate()
                    stopped_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if stopped_count > 0:
            console.print(f"[green]Stopped {stopped_count} API server(s)[/green]")
        else:
            console.print("[yellow]No running API servers found[/yellow]")
            
    except ImportError:
        console.print("[red]psutil not available - install with: pip install psutil[/red]")
        console.print("[yellow]Alternative: Use Ctrl+C in the terminal running the server[/yellow]")
    except Exception as e:
        console.print(f"[red]Error stopping servers: {e}[/red]")


@api.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to")
@click.option("--port", default=5000, type=int, help="Port to bind to")  
@click.option("--debug", is_flag=True, help="Enable debug mode")
def restart(host, port, debug):
    """Restart the Flask API server (stop + start)"""
    console.print("[blue]Restarting API server...[/blue]")
    
    # Stop existing servers
    stop.callback()
    
    # Wait a moment for cleanup
    import time
    time.sleep(1)
    
    # Start new server
    start.callback(host, port, debug, reload=True, no_reload=False)


@api.command()
def status():
    """Check API server status"""
    import requests
    
    try:
        response = requests.get("http://127.0.0.1:5000/", timeout=5)
        if response.status_code == 200:
            console.print("[green]✅ API server is running and accessible[/green]")
            
            # Test API endpoints
            api_response = requests.get("http://127.0.0.1:5000/api/v1/instruments?limit=1", timeout=5)
            if api_response.status_code == 200:
                console.print("[green]✅ API endpoints are working[/green]")
            else:
                console.print(f"[yellow]⚠️ API endpoints returning status {api_response.status_code}[/yellow]")
        else:
            console.print(f"[yellow]⚠️ Server responding with status {response.status_code}[/yellow]")
    
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ API server not accessible on localhost:5000[/red]")
    except requests.exceptions.Timeout:
        console.print("[red]❌ API server timeout[/red]")
    except Exception as e:
        console.print(f"[red]❌ Error checking server status: {e}[/red]")


@api.command()
@click.option("--format", default="table", type=click.Choice(["table", "json"]), help="Output format")
def info(format):
    """Show API server information and available endpoints"""
    from ...config import DATABASE_TYPE
    
    if format == "json":
        import json
        info_data = {
            "api_version": "v1",
            "base_url": "http://127.0.0.1:5000/api/v1",
            "endpoints": {
                "instruments": "/instruments",
                "instrument_detail": "/instruments/{isin}",
                "instrument_raw": "/instruments/{isin}/raw",
                "transparency": "/transparency",
                "entities": "/entities",
                "mic": "/mic"
            },
            "database_type": DATABASE_TYPE,
            "environment": os.environ.get("FLASK_ENV", "production")
        }
        console.print(json.dumps(info_data, indent=2))
    else:
        console.print("[bold blue]MarketDataAPI Server Information[/bold blue]")
        console.print(f"API Version: [green]v1[/green]")
        console.print(f"Base URL: [cyan]http://127.0.0.1:5000/api/v1[/cyan]")
        console.print(f"Database: [yellow]{DATABASE_TYPE}[/yellow]")
        console.print(f"Environment: [yellow]{os.environ.get('FLASK_ENV', 'production')}[/yellow]")
        
        console.print("\n[bold blue]Available Endpoints:[/bold blue]")
        endpoints = [
            ("GET /instruments", "List instruments with filtering"),
            ("GET /instruments/{isin}", "Get instrument details"),
            ("GET /instruments/{isin}/raw", "Get raw model data for comparison"),
            ("GET /transparency", "Transparency calculations"),
            ("GET /entities", "Legal entities"),
            ("GET /mic", "Market identification codes"),
        ]
        
        from rich.table import Table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Endpoint")
        table.add_column("Description")
        
        for endpoint, description in endpoints:
            table.add_row(endpoint, description)
        
        console.print(table)
