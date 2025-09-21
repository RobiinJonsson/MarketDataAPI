#!/bin/bash
# MarketDataAPI Installation Script for Linux/macOS

set -e

echo "🚀 MarketDataAPI Installation Script"
echo "===================================="

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "📋 Python version: $python_version"

if [[ "$(printf '%s\n' "3.8" "$python_version" | sort -V | head -n1)" != "3.8" ]]; then
    echo "❌ Python 3.8 or higher is required. Please upgrade Python."
    exit 1
fi

# Create virtual environment
echo "🔧 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install package
echo "🔨 Installing MarketDataAPI..."
pip install -e .

# Initialize database
echo "💾 Initializing database..."
mkdir -p data logs downloads

# Run alembic migrations if needed
if [ -f "alembic.ini" ]; then
    echo "🗃️  Running database migrations..."
    alembic upgrade head
fi

echo "✅ Installation complete!"
echo ""
echo "🎯 Usage:"
echo "  Activate environment: source venv/bin/activate"
echo "  CLI usage: marketdata --help"
echo "  Short alias: mapi --help"
echo ""
echo "🌐 To start the web API:"
echo "  flask run --host=0.0.0.0 --port=5000"
echo ""
echo "📚 Check README.md for detailed usage instructions."
