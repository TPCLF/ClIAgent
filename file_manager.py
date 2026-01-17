import os
import logging
from pathlib import Path
from typing import Optional, List

logger = logging.getLogger(__name__)


class FileManager:
    """Manage file operations for the agent."""
    
    @staticmethod
    def create_file(filepath: str, content: str, overwrite: bool = False) -> bool:
        """
        Create a file with given content.
        
        Args:
            filepath: Path to the file
            content: File content
            overwrite: Whether to overwrite existing file
        
        Returns:
            True on success, False on failure
        """
        try:
            path = Path(filepath)
            
            if path.exists() and not overwrite:
                logger.warning(f"File already exists: {filepath}")
                return False
            
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
            logger.info(f"✅ File created: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to create file: {e}")
            return False
    
    @staticmethod
    def edit_file(filepath: str, content: str, append: bool = False) -> bool:
        """
        Edit or append to a file.
        
        Args:
            filepath: Path to the file
            content: Content to write or append
            append: Whether to append (True) or overwrite (False)
        
        Returns:
            True on success, False on failure
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                logger.error(f"File does not exist: {filepath}")
                return False
            
            if append:
                with open(path, 'a') as f:
                    f.write('\n' + content)
                logger.info(f"📝 Content appended to: {filepath}")
            else:
                path.write_text(content)
                logger.info(f"📝 File updated: {filepath}")
            
            return True
        except Exception as e:
            logger.error(f"Failed to edit file: {e}")
            return False
    
    @staticmethod
    def read_file(filepath: str) -> Optional[str]:
        """
        Read file content.
        
        Args:
            filepath: Path to the file
        
        Returns:
            File content or None on error
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                logger.error(f"File does not exist: {filepath}")
                return None
            
            return path.read_text()
        except Exception as e:
            logger.error(f"Failed to read file: {e}")
            return None
    
    @staticmethod
    def list_files(directory: str = ".") -> List[str]:
        """
        List files in directory.
        
        Args:
            directory: Directory path
        
        Returns:
            List of file paths
        """
        try:
            path = Path(directory)
            files = [str(f.relative_to(directory)) for f in path.rglob('*') if f.is_file()]
            return sorted(files)
        except Exception as e:
            logger.error(f"Failed to list files: {e}")
            return []
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """
        Delete a file.
        
        Args:
            filepath: Path to the file
        
        Returns:
            True on success, False on failure
        """
        try:
            path = Path(filepath)
            
            if not path.exists():
                logger.error(f"File does not exist: {filepath}")
                return False
            
            path.unlink()
            logger.info(f"🗑️  File deleted: {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete file: {e}")
            return False
