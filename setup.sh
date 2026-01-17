#!/bin/bash
# CLIAgent Setup Script

echo "🚀 Setting up CLIAgent..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python $python_version detected"

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create state directory
mkdir -p .agent_state
echo "📁 State directory created"

# Make main.py executable
chmod +x main.py

echo ""
echo "✨ Setup complete!"
echo ""
echo "📌 Next steps:"
echo "1. Start Ollama: ollama serve"
echo "2. Pull a model: ollama pull mistral"
echo "3. Run the agent: python main.py interactive"
echo ""
