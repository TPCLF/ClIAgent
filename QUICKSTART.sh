#!/bin/bash
# Quick Start Guide for CLIAgent

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║       🤖 CLIAgent Quick Start          ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${YELLOW}Step 1: Install Dependencies${NC}"
echo "Run once to set up:"
echo -e "${GREEN}pip install -r requirements.txt${NC}"
echo ""

echo -e "${YELLOW}Step 2: Start Ollama${NC}"
echo "In a separate terminal:"
echo -e "${GREEN}ollama serve${NC}"
echo ""

echo -e "${YELLOW}Step 3: Pull a Model${NC}"
echo "In another terminal:"
echo -e "${GREEN}ollama pull mistral${NC}"
echo "# or try: neural-chat, dolphin-mixtral, openchat"
echo ""

echo -e "${YELLOW}Step 4: Run CLIAgent${NC}"
echo ""
echo "Interactive Mode (recommended for exploration):"
echo -e "${GREEN}python main.py interactive${NC}"
echo ""
echo "Or execute a single task:"
echo -e "${GREEN}python main.py task \"Your prompt here\"${NC}"
echo ""
echo "With specific model:"
echo -e "${GREEN}python main.py task --model mistral \"Your prompt here\"${NC}"
echo ""

echo -e "${YELLOW}Common Commands:${NC}"
echo -e "${GREEN}python main.py models${NC}        # See available models"
echo -e "${GREEN}python main.py status${NC}        # Show agent status"
echo -e "${GREEN}python main.py interactive${NC}   # Start interactive session"
echo ""

echo -e "${YELLOW}Example Tasks:${NC}"
echo "  'Create a Python function to sort an array'"
echo "  'Write a Dockerfile for a Node.js app'"
echo "  'Debug this Python code: ...'"
echo "  'Generate a regex pattern to validate emails'"
echo ""

echo -e "${GREEN}✨ Everything is ready! Start with Step 2 above.${NC}"
