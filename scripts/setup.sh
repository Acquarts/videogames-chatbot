#!/bin/bash

# Setup script for Videogames Chatbot

set -e

echo "🎮 Videogames Chatbot - Setup Script"
echo "===================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python $required_version or higher is required. Found: $python_version"
    exit 1
fi
echo "✅ Python $python_version found"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ Pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys:"
    echo "   - ANTHROPIC_API_KEY"
    echo "   - STEAM_API_KEY"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create directories
echo "Creating necessary directories..."
mkdir -p chroma_db logs
echo "✅ Directories created"
echo ""

# Check API keys
if grep -q "your_claude_api_key_here" .env || grep -q "your_steam_api_key_here" .env; then
    echo "⚠️  WARNING: API keys not configured!"
    echo "   Please edit .env file and add your API keys"
else
    echo "✅ API keys configured"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in .env file"
echo "2. Run: python -m uvicorn src.main:app --reload"
echo "3. Open: http://localhost:8000/docs"
echo ""
