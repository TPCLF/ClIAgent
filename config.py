import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration manager for the CLI agent."""
    
    def __init__(self):
        self.ollama_host = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
        self.default_model = os.getenv('DEFAULT_MODEL', 'mistral')
        self.state_dir = Path(os.getenv('STATE_DIR', './.agent_state'))
        self.state_dir.mkdir(exist_ok=True)
        self.current_session_file = self.state_dir / "current_session.json"
        self.session_archive_file = self.state_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def get_session_state(self) -> Dict[str, Any]:
        """Load current session state, or create new one."""
        if self.current_session_file.exists():
            try:
                with open(self.current_session_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Current session file corrupted, starting fresh")
        return self._create_blank_state()
    
    def _create_blank_state(self) -> Dict[str, Any]:
        """Create blank session state."""
        return {
            "messages": [],
            "files_created": [],
            "files_modified": [],
            "project_context": "",
            "current_working_dir": str(Path.cwd()),
            "session_start": datetime.now().isoformat()
        }
    
    def save_session_state(self, state: Dict[str, Any]):
        """Save session state to current session file (in-memory persistence)."""
        with open(self.current_session_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def archive_session(self) -> str:
        """Archive current session to timestamped file."""
        if self.current_session_file.exists():
            with open(self.current_session_file, 'r') as f:
                state = json.load(f)
            
            with open(self.session_archive_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"📦 Session archived to {self.session_archive_file.name}")
            return str(self.session_archive_file)
        return None
    
    def reset_session(self):
        """Clear current session (start fresh)."""
        if self.current_session_file.exists():
            self.archive_session()
            self.current_session_file.unlink()
            logger.info("🔄 Session reset - starting fresh")


config = Config()
