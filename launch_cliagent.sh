#!/bin/bash
# Launch script for CLIAgent desktop launcher
# Opens gnome-terminal and starts the interactive agent

cd /home/user/CLIAgent

# Launch gnome-terminal with the interactive agent
gnome-terminal -- bash -c '
    cd /home/user/CLIAgent
    echo "🤖 Starting CLIAgent..."
    echo ""
    python3 main.py interactive
    echo ""
    echo "Press Enter to close..."
    read
'
