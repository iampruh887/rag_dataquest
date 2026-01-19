#!/bin/bash

echo "🚀 Starting Financial AI Agent UI"
echo "=================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Load environment variables
if [ -f .env ]; then
    echo "Loading environment variables..."
    export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
fi

# Check data directory
if [ -d "moneycontrol_news" ]; then
    file_count=$(ls moneycontrol_news/*.json 2>/dev/null | wc -l)
    echo "✅ Found moneycontrol_news with $file_count JSON files"
else
    echo "⚠️  moneycontrol_news directory not found"
fi

# Check API key
if [ -n "$GOOGLE_API_KEY" ]; then
    echo "✅ Google API key loaded"
else
    echo "⚠️  GOOGLE_API_KEY not set (will run in RAG-only mode)"
fi

echo ""
echo "Starting UI on http://localhost:7864"
echo "===================================="
echo ""
echo "Features:"
echo "- 💬 Interactive chat with AI"
echo "- 📊 Company analysis"
echo "- 🌍 Market summaries"
echo "- 🔍 Real-time financial news context"
echo ""
echo "Press Ctrl+C to stop"
echo ""

python ui.py