# Getting Started with CLIAgent

## 🚀 Prerequisites

- Python 3.8 or higher
- Ollama installed on your system
- Internet connection (optional, for web features)
- 2GB+ RAM for running LLMs

## 📋 Installation

### Step 1: Install Python Dependencies

```bash
cd /home/user/CLIAgent
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
python main.py --help
```

You should see the CLI help output with available commands.

## 🤖 Setting Up Ollama

### Step 1: Install Ollama

Download from [ollama.ai](https://ollama.ai) or use package manager:

```bash
# macOS/Linux with Homebrew
brew install ollama

# Or download directly from ollama.ai
```

### Step 2: Start Ollama Server

Open a new terminal and run:

```bash
ollama serve
```

You should see output like:
```
Listening on 127.0.0.1:11434
```

### Step 3: Pull a Model

In another terminal, download a model:

```bash
# Recommended for coding
ollama pull mistral

# Or try these alternatives
ollama pull neural-chat
ollama pull dolphin-mixtral
ollama pull openchat
```

The first download may take a few minutes depending on model size.

## 🎮 Your First Interaction

### Interactive Mode (Recommended)

```bash
python main.py interactive
```

Example session:
```
➜ Create a Python function to validate an email
[Agent processes and generates code]

➜ Write a REST API in Node.js
[Agent creates Node.js code]

➜ status
[Shows agent and system info]

➜ exit
```

### Single Command Mode

```bash
python main.py task "Write a Python script that sorts a list"
```

### With Specific Model

```bash
python main.py task --model mistral "Create a React component for a button"
```

## 📚 Common Commands

### List Models
```bash
python main.py models
```

### Check Status
```bash
python main.py status
```

### View Help
```bash
python main.py --help
python main.py interactive --help
python main.py task --help
```

### Direct File Creation
```bash
python main.py create myfile.py "print('hello')" --overwrite
```

## 💡 Usage Tips

### 1. Be Specific with Prompts
**Good:** "Create a Python function that takes a list and returns the sum of all even numbers"
**Bad:** "Python function"

### 2. Use Model-Specific Tasks
- **Mistral**: Great for reasoning and coding
- **Neural-Chat**: Excellent conversational abilities
- **Dolphin**: Strong at complex problem solving

### 3. Switch Models on the Fly
```
➜ model:neural-chat
Model switched to: neural-chat
```

### 4. Check Session History
Session files are saved in `.agent_state/` with timestamps

### 5. Combine Commands
```bash
python main.py task --model dolphin "Debug this code snippet: [code]"
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` to customize:

```bash
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=mistral
STATE_DIR=./.agent_state
```

### Custom State Directory

```bash
export STATE_DIR=/custom/path
python main.py interactive
```

## 📝 Examples

### Example 1: Generate Code

```bash
python main.py task "Create a Python decorator that measures function execution time"
```

### Example 2: Write Configuration Files

```bash
python main.py task "Generate a Dockerfile for a Python Flask application"
```

### Example 3: Debug Help

```bash
python main.py task "Why might this Python code be slow? [code snippet here]"
```

### Example 4: Learning

```bash
python main.py task "Explain how closures work in JavaScript with examples"
```

## 🔍 Troubleshooting

### "Ollama is not running"
- Make sure Ollama server is started: `ollama serve`
- Check if it's on correct host/port (default: localhost:11434)
- Verify with: `curl http://localhost:11434/api/tags`

### "No models found"
- Pull a model: `ollama pull mistral`
- List available: `ollama list`

### "Python dependency errors"
- Reinstall dependencies: `pip install --upgrade -r requirements.txt`
- Use a virtual environment: `python -m venv venv && source venv/bin/activate`

### "Permission denied" on scripts
- Make executable: `chmod +x main.py setup.sh`

### "Out of memory"
- Smaller models use less RAM: try `neural-chat` instead of larger models
- Monitor with: `top` or `htop`

## 📖 Documentation

- [README.md](README.md) - Full feature documentation
- [ARCHITECTURE.md](ARCHITECTURE.md) - System design and internals
- [examples.py](examples.py) - Programmatic usage examples

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Start Ollama server
3. ✅ Pull a model
4. ✅ Try interactive mode
5. ✅ Explore different prompts
6. ✅ Check session history
7. ✅ Try switching models

## 💬 Interactive Mode Guide

### Main Features

**Thinking Workflow:**
```
1. 💭 Thinking  - Agent analyzes your request
2. 📋 Planning  - Creates detailed plan
3. ✨ Implementation - Generates solution
```

**Available Commands:**
- `help` - Show help
- `status` - Show agent status
- `models` - List available models
- `model:<name>` - Switch model
- `exit/quit` - Exit
- Any other text is treated as a prompt

### Tips for Best Results

1. **Start simple:** "Write hello world in Python"
2. **Be descriptive:** Include context, requirements, constraints
3. **Reference existing code:** Paste snippets for debugging
4. **Ask for formats:** "Generate as JSON", "Use classes", etc.
5. **Follow up:** "Make it more efficient", "Add error handling"

## 🚀 Advanced Usage

### Programmatic Usage

```python
from agent import Agent

agent = Agent(model="mistral")
result = agent.execute("Write a quicksort implementation")
print(result["implementation"])
```

### File Operations

```python
# Create
agent.create_file("script.py", "print('test')")

# Read
content = agent.read_file("script.py")

# Edit
agent.edit_file("script.py", "\nprint('updated')", append=True)

# Delete
agent.delete_file("script.py")
```

### Web Access

```python
# Fetch
content = agent.fetch_web("https://example.com")

# Search
results = agent.search_web("Python best practices")
```

## 📊 Performance Notes

- **First run:** May take 10-30s as model loads
- **Subsequent runs:** 5-15s depending on model and hardware
- **Large prompts:** May take longer, but usually completes within 30s
- **Smaller models:** Faster but less capable
- **Larger models:** Slower but more powerful

## 💾 Session Management

Sessions are automatically saved:
- **Location:** `.agent_state/session_YYYYMMDD_HHMMSS.json`
- **Contains:** All prompts, responses, files created/modified
- **Persistence:** Automatic, no action needed

Load previous session:
```bash
cat .agent_state/session_*.json | jq .
```

## ✨ Best Practices

1. ✅ Use descriptive prompts
2. ✅ Start with simpler requests
3. ✅ Check status if unsure
4. ✅ Review generated code before using
5. ✅ Keep sessions organized
6. ✅ Pull models that match your use case
7. ✅ Monitor system resources

## 🆘 Getting Help

1. Check `main.py --help` for CLI options
2. Read [README.md](README.md) for features
3. View [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
4. Check session history for context
5. Run `python examples.py` for usage patterns

## 🎓 Learning Resources

- Ollama documentation: https://ollama.ai
- Python Click docs: https://click.palletsprojects.com/
- LLM best practices: Research papers on prompt engineering

---

**You're all set! Start with:**
```bash
python main.py interactive
```

**Happy coding! 🚀**
