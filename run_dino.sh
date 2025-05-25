#!/bin/bash

# DINO Project Launch Script
# Ensures proper virtual environment activation

echo "🦕 Starting DINO Project..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "💡 Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
if ! python -c "import google.generativeai, streamlit" 2>/dev/null; then
    echo "❌ Required packages not found!"
    echo "💡 Please run: pip install -r requirements.txt"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "💡 Create .env file with: GEMINI_API_KEY=your_api_key_here"
fi

echo "🚀 Starting Streamlit app..."
echo "📱 Open browser at: http://localhost:8501"
echo "🛑 Press Ctrl+C to stop"

# Run streamlit
python -m streamlit run streamlit_app.py 