# MarketData CLI Usage Guide

## CLI Access Methods

The MarketDataAPI CLI can be accessed through several methods:

### 1. Recommended: Use Wrapper Scripts (Works from any directory)

For cross-platform compatibility and reliable database path resolution:

```bash
# Windows Batch (recommended for Windows)
C:\path\to\MarketDataAPI\deployment\mapi.bat instruments list --limit 5

# PowerShell (Windows)
powershell -ExecutionPolicy Bypass -File "C:\path\to\MarketDataAPI\deployment\mapi.ps1" instruments list --limit 5

# Direct module execution (cross-platform)
cd C:\path\to\MarketDataAPI
python -m marketdata_api.cli instruments list --limit 5
```

### 2. Global Command (with environment variable)

If you installed the package globally (`pip install -e .`), you need to set the database path:

```powershell
# PowerShell (set for session)
$env:SQLITE_DB_PATH="C:\path\to\MarketDataAPI\src\marketdata_api\database\marketdata.db"
marketdata instruments list --limit 5

# Command Prompt (set for session)
set SQLITE_DB_PATH=C:\path\to\MarketDataAPI\src\marketdata_api\database\marketdata.db
marketdata instruments list --limit 5
```

### 3. Permanent Environment Variable (Windows)

To set permanently (requires restart of terminal):

```powershell
# PowerShell (as Administrator)
[Environment]::SetEnvironmentVariable("SQLITE_DB_PATH", "C:\Users\robin\Projects\MarketDataAPI\src\marketdata_api\database\marketdata.db", "User")

# Then restart terminal and use:
marketdata instruments list --limit 5
```

## Troubleshooting

### "no such table: instruments" Error

This error occurs when the CLI cannot find the database file. Solutions:

1. **Reinstall in development mode** (recommended for developers):
   ```bash
   pip uninstall marketdata-api -y
   pip install -e .
   ```
2. **Use wrapper scripts** (always works regardless of installation):
   - `mapi.bat` or `mapi.ps1` scripts
3. **Set SQLITE_DB_PATH** environment variable to full path
4. **Run from project directory** where .env file exists

**Note**: If you installed the package with `pip install .` (without `-e`), it copies files at installation time and won't reflect recent changes. Always use `pip install -e .` for development.

### Database Path Issues

The CLI tries to find the database in this order:
1. SQLITE_DB_PATH environment variable
2. .env file in various locations (project root, current directory)
3. Default calculated path (may not work for global installs)

## Examples

```bash
# List instruments
mapi.bat instruments list --limit 10

# Search by ISIN
mapi.bat instruments search US0378331005

# Show transparency data
mapi.bat transparency calculate US0378331005

# Database statistics
mapi.bat stats

# Initialize database (if needed)
mapi.bat init --force
```

## Path Configuration

The database path is configured in `.env` file:
```
SQLITE_DB_PATH=C:\Users\robin\Projects\MarketDataAPI\src\marketdata_api\database\marketdata.db
```

Make sure this path is absolute and points to your actual database file.
