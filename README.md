# CLIAgent - Terminal AI Coding Agent

A clean, simple terminal-based AI coding agent that leverages your local Ollama LLMs with file creation/editing capabilities and internet access.

## Features

✨ **Core Features:**
- 🤖 Integration with local Ollama LLMs
- 💭 Think-Prepare-Implement workflow for better responses
- 📝 Create and edit files dynamically
- 🌐 Web access and searching
- 💾 Persistent session state
- 🎯 Interactive and command modes

## Requirements

- Python 3.8+
- Ollama running locally (`ollama serve`)
- Internet connection (optional, for web features)

## Installation

```bash
cd /home/user/CLIAgent
pip install -r requirements.txt
chmod +x main.py
```

## Setup

1. **Start Ollama:**
   ```bash
   ollama serve
   ```

2. **Pull a model (in another terminal):**
   ```bash
   ollama pull mistral  # or your preferred model
   ```

## Usage

### Interactive Mode
```bash
python main.py interactive
```

Commands in interactive mode:
- `help` - Show available commands
- `status` - Show agent status
- `models` - List available models
- `model:<name>` - Switch to a different model
- `<any prompt>` - Execute task with AI
- `exit` - Quit

### Execute Single Task
```bash
python main.py task "Create a Python script that generates fibonacci numbers"

# With specific model
python main.py task --model mistral "Write a hello world in Rust"
```

### Quick Commands
```bash
# List available models
python main.py models

# Show status
python main.py status

# Create a file directly
python main.py create myfile.py "print('Hello')" --overwrite
```

## Configuration

Set environment variables to customize:

```bash
export OLLAMA_HOST="http://localhost:11434"  # Ollama server URL
export DEFAULT_MODEL="mistral"               # Default LLM model
export STATE_DIR="./.agent_state"            # Session state directory
```

## Architecture

```
main.py           - CLI entry point
agent.py          - Main Agent orchestrator
ollama_client.py  - Ollama LLM integration
file_manager.py   - File operations
web_client.py     - Web access
config.py         - Configuration management
```

## Workflow: Think-Prepare-Implement

Each task goes through three stages:

1. **💭 Thinking** - Analyze and understand the request
2. **📋 Planning** - Create a detailed step-by-step plan
3. **✨ Implementation** - Execute with code/instructions

This ensures thoughtful, well-structured responses.

## Example Session

```bash
$ python main.py interactive
[Header displayed]

➜ Create a Python function to reverse a string without using slicing

💭 Thinking: [Analysis of the problem]

📋 Plan: [Step-by-step plan]

✨ Implementation:
def reverse_string(s):
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result += s[i]
    return result
```

## Session Persistence

Session state is automatically saved to `.agent_state/session_YYYYMMDD_HHMMSS.json` with:
- All prompts and responses
- Files created/modified
- Conversation history

## Tips

- Use specific, detailed prompts for better results
- Start with `mistral` or `neural-chat` for coding tasks
- Check available models before switching
- Session history is saved automatically
- Use `model:<name>` to quickly switch models

## License

MIT

## Author

Built with ❤️ for 10x engineers
