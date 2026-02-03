#!/bin/bash
# Quick setup script for AEval Backend

set -e

echo "🚀 Setting up AEval Backend..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org -q
pip install -r requirements.txt --index-url https://pypi.org/simple/ --trusted-host pypi.org --trusted-host files.pythonhosted.org

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your ZAI_API_KEY before running the server!"
    echo ""
    echo "Edit .env with:"
    echo "  nano .env"
    echo "  # or"
    echo "  vim .env"
    echo ""
else
    echo "✅ .env file already exists"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Make sure .env is configured with your API key"
echo "  2. Run: source venv/bin/activate"
echo "  3. Run: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "API will be available at: http://localhost:8000"
echo "API docs at: http://localhost:8000/docs"
