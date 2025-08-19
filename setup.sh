#!/bin/bash

# AI Flashcard Creator Setup Script
echo "🧠 AI Flashcard Creator Setup"
echo "=============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed."
    exit 1
fi

echo "✅ pip3 found"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and fill in your API keys:"
echo "   cp .env.example .env"
echo ""
echo "2. Set up Firebase:"
echo "   - Create a Firebase project at https://console.firebase.google.com"
echo "   - Enable Authentication (Email/Password)"
echo "   - Enable Firestore Database"
echo "   - Download service account key as firebase_key.json"
echo ""
echo "3. Get Groq API key:"
echo "   - Sign up at https://console.groq.com"
echo "   - Create an API key"
echo "   - Add it to your .env file"
echo ""
echo "4. Run the application:"
echo "   source .venv/bin/activate"
echo "   python app.py"
echo ""
echo "Happy learning! 🚀"
