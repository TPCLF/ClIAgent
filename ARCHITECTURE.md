## CLIAgent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    main.py (CLI Interface)                  │
│  Interactive & command modes, user interaction layer        │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    agent.py     ollama_client.py   file_manager.py
    (Orchestrator) (LLM Integration) (File Operations)
        │              │              │
        └──────────────┼──────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
    web_client.py   config.py    session state
  (Web Access)  (Configuration) (Persistence)
```

### Module Breakdown

#### `main.py` - CLI Entry Point
- Command-line interface using Click
- Interactive mode for conversation
- Single task execution
- Model management
- Colorized output for better UX

#### `agent.py` - Core Agent Logic
- Orchestrates all components
- Maintains session state
- Handles tool calls
- Implements think-prepare-implement workflow
- File and web operations wrapper

#### `ollama_client.py` - LLM Integration
- Communicates with Ollama API
- Model management (list, switch)
- Text generation with streaming support
- Implements 3-stage thinking process
- Error handling for LLM calls

#### `file_manager.py` - File Operations
- Create files safely
- Edit/append content
- Read file content
- Delete files
- List directory contents
- All operations are logged

#### `web_client.py` - Web Integration
- Fetch web pages
- Search functionality (DuckDuckGo)
- Timeout and error handling
- User-Agent headers

#### `config.py` - Configuration Management
- Environment variable loading
- Session state management
- Persistent storage
- Default configurations

### Data Flow

```
User Input (CLI)
       │
       ▼
Agent.execute()
       │
       ├─→ think_prepare_implement()
       │    ├─→ Ollama: Analyze request
       │    ├─→ Ollama: Create plan
       │    └─→ Ollama: Generate solution
       │
       ├─→ Tool Calls (optional)
       │    ├─→ FileManager operations
       │    └─→ WebClient operations
       │
       ▼
Session State (persisted)
       │
       ▼
Output to User
```

### Session Persistence

Sessions are automatically saved to `.agent_state/session_YYYYMMDD_HHMMSS.json` containing:
```json
{
  "messages": [
    {
      "prompt": "user request",
      "result": {
        "thinking": "...",
        "plan": "...",
        "implementation": "..."
      }
    }
  ],
  "files_created": ["file1.py", "file2.md"],
  "files_modified": ["config.py"]
}
```

### Key Design Principles

1. **Simplicity** - Clean, focused modules with single responsibilities
2. **Persistence** - All sessions and actions automatically saved
3. **Transparency** - All steps visible (thinking → planning → implementation)
4. **Extensibility** - Easy to add new tools and capabilities
5. **Robustness** - Comprehensive error handling and logging
6. **User-Friendly** - Colorized output, clear prompts, helpful messages

### Dependencies

- `click` - CLI framework
- `colorama` - Cross-platform colored terminal text
- `requests` - HTTP library for web and Ollama API
- `python-dotenv` - Environment variable management

### Performance Characteristics

- **Startup time**: ~100ms (CLI only)
- **LLM response time**: 5-30s depending on model and hardware
- **File operations**: <10ms
- **Web fetch**: 1-5s depending on page size

### Scalability & Future Extensions

The architecture supports:
- Multi-model coordination
- Tool chaining
- Context windows management
- Fine-tuning prompts
- Custom tool plugins
- Batch processing
- API server mode
