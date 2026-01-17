# CLIAgent Desktop Launcher for Ubuntu Gnome

## Installation

The desktop launcher has been automatically installed to:
```
~/.local/share/applications/cliagent.desktop
```

## How to Use

### Method 1: Applications Menu (Recommended)
1. Press the **Super key** (Windows key) to open Activities
2. Search for **"CLIAgent"**
3. Click on the **CLIAgent** application
4. A terminal window will open with the interactive agent ready to use

### Method 2: Command Line
```bash
/home/user/CLIAgent/launch_cliagent.sh
```

### Method 3: Direct Terminal
```bash
cd /home/user/CLIAgent
python3 main.py interactive
```

## What Happens When You Launch

1. ✅ A terminal window opens automatically
2. ✅ CLIAgent starts in interactive mode
3. ✅ You're immediately ready to give prompts
4. ✅ The agent thinks, plans, and implements automatically
5. ✅ Files are created and folders are organized

## Features

🤖 **Direct Terminal Access**
- Interact with the LLM agent instantly
- See real-time responses
- Monitor file creation

💭 **Think-Prepare-Implement Workflow**
- Agent analyzes your request
- Creates a detailed plan
- Executes and generates code

📝 **Auto-Execution**
- Files are created automatically
- Folders are organized
- No manual steps needed

## Troubleshooting

### Launcher doesn't appear in Applications menu
1. Clear the applications cache:
   ```bash
   rm -f ~/.cache/desktop-files/*
   ```
2. Log out and log back in, or restart

### Terminal doesn't open
1. Verify gnome-terminal is installed:
   ```bash
   which gnome-terminal
   ```
2. If not, install it:
   ```bash
   sudo apt install gnome-terminal
   ```

### Agent doesn't start
1. Make sure Ollama is running:
   ```bash
   ollama serve
   ```
   (in a separate terminal)

2. Check if a model is available:
   ```bash
   ollama pull mistral
   ```

## Advanced: Customize the Launcher

### Change the Icon
Edit `~/.local/share/applications/cliagent.desktop` and change:
```ini
Icon=utilities-terminal
```

To any icon name like:
- `Icon=text-editor`
- `Icon=accessories-text-editor`
- Or a full path: `Icon=/path/to/icon.png`

### Add a Keyboard Shortcut
1. Open **Settings** → **Keyboard** → **Shortcuts**
2. Scroll down to "Custom Shortcuts"
3. Click **"+"** to add new
4. Name: `CLIAgent`
5. Command: `/home/user/CLIAgent/launch_cliagent.sh`
6. Set a keyboard shortcut (e.g., `Ctrl+Alt+C`)

### Create a Desktop Shortcut
```bash
cp ~/.local/share/applications/cliagent.desktop ~/Desktop/
```

Then right-click on the desktop file and select "Allow Launching".

## Files

- `cliagent.desktop` - The desktop launcher entry
- `launch_cliagent.sh` - Shell script that opens the terminal
- `main.py` - CLI entry point

## Support

For issues or questions:
- Check `README.md` for features
- Read `GETTING_STARTED.md` for setup
- View `ARCHITECTURE.md` for technical details

---

**You're all set!** Press the Super key and search for "CLIAgent" to launch. 🚀
