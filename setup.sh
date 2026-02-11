#!/bin/bash
set -e  # Exit on error

echo "Setting up pre-commit hooks for Jekyll blog..."

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

# installing dependencies
sudo dnf install ImageMagick

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install pre-commit
echo "Installing pre-commit..."
pip install --upgrade pip
pip install pre-commit

# Make the hook executable
echo "Making hook script executable..."
chmod +x hooks/jekyll-tabs-formatter.py

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

echo ""
echo "✓ Setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
echo "  source .venv/bin/activate"
