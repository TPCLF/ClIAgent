import requests
import logging
from typing import Dict, Any, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class WebClient:
    """Client for web access and searching."""
    
    @staticmethod
    def fetch(url: str, timeout: int = 10) -> Optional[str]:
        """
        Fetch content from a URL.
        
        Args:
            url: The URL to fetch
            timeout: Request timeout in seconds
        
        Returns:
            Page content or None on error
        """
        try:
            headers = {
                'User-Agent': 'CLIAgent/1.0'
            }
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    @staticmethod
    def search(query: str) -> Optional[str]:
        """
        Search the web (basic implementation with DuckDuckGo).
        
        Args:
            query: Search query
        
        Returns:
            Search results
        """
        try:
            url = "https://html.duckduckgo.com/"
            params = {"q": query}
            headers = {
                'User-Agent': 'CLIAgent/1.0'
            }
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            logger.info(f"Search results fetched for: {query}")
            return response.text[:5000]  # Limit response size
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return None
