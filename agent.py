import logging
import re
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
from ollama_client import OllamaClient, think_prepare_implement
from file_manager import FileManager
from web_client import WebClient
from config import config

logger = logging.getLogger(__name__)


class Agent:
    """Main AI Agent for executing tasks."""
    
    def __init__(self, model: str = None):
        self.client = OllamaClient(model=model)
        self.file_manager = FileManager
        self.web = WebClient
        self.session_state = config.get_session_state()
        self.tools = {
            "create_file": self.create_file,
            "edit_file": self.edit_file,
            "read_file": self.read_file,
            "list_files": self.list_files,
            "delete_file": self.delete_file,
            "fetch_web": self.fetch_web,
            "search_web": self.search_web,
            "set_model": self.set_model,
        }
    
    def create_file(self, filepath: str, content: str, overwrite: bool = False) -> bool:
        """Create a file."""
        result = self.file_manager.create_file(filepath, content, overwrite)
        if result:
            self.session_state["files_created"].append(filepath)
            self._save_state()
        return result
    
    def edit_file(self, filepath: str, content: str, append: bool = False) -> bool:
        """Edit a file."""
        result = self.file_manager.edit_file(filepath, content, append)
        if result:
            self.session_state["files_modified"].append(filepath)
            self._save_state()
        return result
    
    def read_file(self, filepath: str) -> str:
        """Read a file."""
        content = self.file_manager.read_file(filepath)
        return content or ""
    
    def list_files(self, directory: str = ".") -> str:
        """List files in directory."""
        files = self.file_manager.list_files(directory)
        return "\n".join(files) if files else "No files found"
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file."""
        return self.file_manager.delete_file(filepath)
    
    def fetch_web(self, url: str) -> str:
        """Fetch web content."""
        content = self.web.fetch(url)
        return content or "Failed to fetch content"
    
    def search_web(self, query: str) -> str:
        """Search the web."""
        results = self.web.search(query)
        return results or "No results found"
    
    def set_model(self, model: str) -> str:
        """Switch to a different model."""
        models = self.client.list_models()
        if model in models:
            self.client.set_model(model)
            return f"✅ Model switched to: {model}"
        return f"❌ Model not found. Available: {', '.join(models)}"
    
    def execute(self, prompt: str, use_workflow: bool = True) -> Dict[str, Any]:
        """
        Execute a task with the agent.
        
        Args:
            prompt: Task description
            use_workflow: Use think-prepare-implement workflow
        
        Returns:
            Execution result
        """
        logger.info(f"🤖 Agent executing: {prompt[:50]}...")
        
        if not self.client.is_available():
            logger.error("❌ Ollama is not running!")
            return {"error": "Ollama not available"}
        
        try:
            # Inject session context into prompt for continuity
            context_prompt = self._build_context_prompt(prompt)
            
            if use_workflow:
                result = think_prepare_implement(context_prompt, client=self.client)
            else:
                result = {
                    "implementation": self.client.generate(context_prompt)
                }
        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            return {"error": str(e)}
        
        # Auto-execute: Parse and create files/folders from implementation
        if "implementation" in result:
            self._auto_execute(result["implementation"])
        
        # Store in session
        self.session_state["messages"].append({
            "prompt": prompt,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        
        # Update project context based on what was created
        self._update_project_context()
        self._save_state()
        
        return result
    
    def _build_context_prompt(self, prompt: str) -> str:
        """Build prompt with session context for memory."""
        context_parts = []
        
        # Add project context if available
        if self.session_state.get("project_context"):
            context_parts.append(f"PROJECT CONTEXT:\n{self.session_state['project_context']}\n")
        
        # Add recent message history (last 5 messages)
        recent_messages = self.session_state.get("messages", [])[-5:]
        if recent_messages:
            context_parts.append("RECENT WORK:")
            for msg in recent_messages:
                context_parts.append(f"- {msg['prompt'][:100]}")
        
        # Add files created in this session
        if self.session_state.get("files_created"):
            context_parts.append(f"\nFILES CREATED THIS SESSION:\n" + 
                               "\n".join(self.session_state["files_created"]))
        
        # Build final prompt with context
        if context_parts:
            return "\n".join(context_parts) + "\n\nCURRENT TASK:\n" + prompt
        return prompt
    
    def _update_project_context(self):
        """Update project context based on created files."""
        if self.session_state.get("files_created"):
            files = self.session_state["files_created"]
            self.session_state["project_context"] = (
                f"Working on project with {len(files)} file(s): {', '.join(files[-5:])}"
            )
    
    
    def _auto_execute(self, implementation: str):
        """
        Parse implementation and auto-execute file/folder creation.
        Extracts code blocks and creates files automatically.
        """
        logger.info("🔨 Auto-executing generated code...")
        
        # Pattern: Look for "mkdir Calc" - handle backticks
        mkdir_pattern = r'`?mkdir\s+([a-zA-Z0-9_\-\.]+)`?'
        mkdir_matches = re.findall(mkdir_pattern, implementation)
        
        # Filter out false positives (single letters, numbers)
        directories = [d for d in set(mkdir_matches) if len(d) > 1]
        
        if directories:
            logger.info(f"📂 Found directories: {', '.join(directories)}")
        
        # Pattern: Code blocks with language specifiers
        code_block_pattern = r'```(?:python|py|javascript|js|json|yaml|yml|bash|sh|html|css|dockerfile)?\n(.*?)```'
        code_blocks = re.findall(code_block_pattern, implementation, re.DOTALL)
        
        if code_blocks:
            logger.info(f"📄 Found {len(code_blocks)} code blocks")
        
        # Pattern: Look for file names mentioned - be specific
        file_pattern = r'([a-zA-Z0-9_\-]+\.(?:py|js|json|txt|html|css|yaml|yml|md|sh))'
        file_matches = re.findall(file_pattern, implementation)
        files_to_create = list(set(file_matches))
        
        if files_to_create:
            logger.info(f"📋 Found files: {', '.join(files_to_create)}")
        
        # Create directories first
        home = os.path.expanduser("~")
        created_dirs = []
        for dir_name in directories:
            # Create in home directory
            dir_path = os.path.join(home, dir_name)
            
            try:
                Path(dir_path).mkdir(parents=True, exist_ok=True)
                logger.info(f"✅ Created directory: {dir_path}")
                created_dirs.append(dir_path)
            except Exception as e:
                logger.error(f"❌ Failed to create directory {dir_path}: {e}")
        
        # Create files with code blocks in the created directories
        if code_blocks and created_dirs:
            # Pair code blocks with files and directories
            for i, code in enumerate(code_blocks):
                try:
                    # Use filename if available, otherwise generate one
                    if i < len(files_to_create):
                        filename = files_to_create[i]
                    else:
                        filename = f"calculator.py" if "tkinter" in code.lower() or "import tk" in code else f"file_{i}.py"
                    
                    # Create in first directory created
                    dir_path = created_dirs[0]
                    filepath = os.path.join(dir_path, filename)
                    content = code.strip()
                    
                    if self.create_file(filepath, content, overwrite=True):
                        logger.info(f"✅ Auto-created file: {filepath}")
                except Exception as e:
                    logger.error(f"❌ Failed to create file: {e}")
                    continue
        elif code_blocks and not created_dirs:
            # No directories found, create in current directory
            for i, code in enumerate(code_blocks):
                try:
                    filename = f"calculator_{i}.py" if "tkinter" in code.lower() else f"file_{i}.py"
                    if self.create_file(filename, code.strip(), overwrite=True):
                        logger.info(f"✅ Auto-created file: {filename}")
                except Exception as e:
                    logger.error(f"❌ Failed to create file: {e}")
                    continue
    
    def _save_state(self):
        """Save session state."""
        config.save_session_state(self.session_state)
    
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return self.client.list_models()
    
    def show_status(self) -> str:
        """Show agent status."""
        models = self.get_available_models()
        status = f"""
╔════════════════════════════════════════╗
║         🤖 CLIAgent Status             ║
╠════════════════════════════════════════╣
║ Ollama Host:      {self.client.host:<20}
║ Active Model:     {self.client.model:<20}
║ Models Available: {len(models):<20}
║ Files Created:    {len(self.session_state['files_created']):<20}
║ Files Modified:   {len(self.session_state['files_modified']):<20}
║ Messages:         {len(self.session_state['messages']):<20}
╚════════════════════════════════════════╝
        """
        return status
