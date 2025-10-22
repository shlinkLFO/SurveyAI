#!/bin/bash
# Installation script for AI Confidence Survey

echo "=== AI Confidence Survey Installation ==="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To start the application:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run server: ./start.sh"
echo "  or: python main.py"
echo "  or: uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "Access at: http://localhost:8000"
echo "Admin panel: http://localhost:8000/admin"
echo ""

