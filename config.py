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
        self.session_file = self.state_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def get_session_state(self) -> Dict[str, Any]:
        """Load session state if exists."""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                return json.load(f)
        return {"messages": [], "files_created": [], "files_modified": []}
    
    def save_session_state(self, state: Dict[str, Any]):
        """Save session state."""
        with open(self.session_file, 'w') as f:
            json.dump(state, f, indent=2)


config = Config()
