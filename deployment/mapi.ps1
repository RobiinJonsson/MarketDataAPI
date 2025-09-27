# MarketData API CLI PowerShell Wrapper
# This script provides a convenient way to run the MarketData API CLI from any directory
# Sets proper environment variables and paths

param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Arguments
)

# Get the directory where this script is located
$ScriptDir = $PSScriptRoot
# Go up one level to project root (deployment -> project root)  
$ProjectRoot = Split-Path $ScriptDir -Parent

# Store current directory
$OriginalPath = Get-Location

try {
    # Change to project directory
    Set-Location $ProjectRoot
    
    # Set environment variables for CLI
    $env:PYTHONPATH = "$ProjectRoot\src;$env:PYTHONPATH"
    $env:SQLITE_DB_PATH = "$ProjectRoot\src\marketdata_api\database\marketdata.db"
    
    # Run the CLI using the module entry point
    & python -m marketdata_api.cli @Arguments
}
finally {
    # Restore original directory
    Set-Location $OriginalPath
}
