#!/bin/bash
set -e  # Exit on error


# Check if rbenv is installed
if ! command -v rbenv &> /dev/null; then
    echo "❌ Error: rbenv is not installed."
    echo "Please install rbenv first:"
    echo "  sudo dnf install -y rbenv ruby-build"
    echo "  echo 'eval \"\$(rbenv init - bash)\"' >> ~/.bashrc"
    echo "  source ~/.bashrc"
    exit 1
fi

# Check if .ruby-version exists
if [ ! -f ".ruby-version" ]; then
    echo "❌ Error: .ruby-version file not found in project directory."
    exit 1
fi

# Read required Ruby version
REQUIRED_RUBY=$(cat .ruby-version)
echo "Required Ruby version: $REQUIRED_RUBY"

# Check if required Ruby version is installed
if ! rbenv versions | grep -q "$REQUIRED_RUBY"; then
    echo "Installing Ruby $REQUIRED_RUBY..."
    rbenv install "$REQUIRED_RUBY"
else
    echo "✓ Ruby $REQUIRED_RUBY is already installed"
fi

# Set local Ruby version
echo "Setting local Ruby version to $REQUIRED_RUBY..."
rbenv local "$REQUIRED_RUBY"

# Verify active Ruby version
ACTIVE_RUBY=$(rbenv version | awk '{print $1}')
if [ "$ACTIVE_RUBY" != "$REQUIRED_RUBY" ]; then
    echo "❌ Error: Failed to set Ruby version to $REQUIRED_RUBY"
    echo "Active version is: $ACTIVE_RUBY"
    exit 1
fi

echo "✓ Ruby $REQUIRED_RUBY is active"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment in .venv..."
    python3 -m venv .venv
fi

# Installing dependencies
echo "Installing system dependencies..."
sudo dnf install -y ImageMagick

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
