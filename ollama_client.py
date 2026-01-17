import requests
import logging
from typing import Optional, Dict, Any
from config import config

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with local Ollama LLMs."""
    
    def __init__(self, host: str = None, model: str = None):
        self.host = host or config.ollama_host
        self.model = model or config.default_model
        self.api_endpoint = f"{self.host}/api/generate"
    
    def list_models(self) -> list:
        """List available models on Ollama."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            response.raise_for_status()
            models = response.json().get('models', [])
            return [m['name'] for m in models]
        except Exception as e:
            logger.error(f"Failed to list models: {e}")
            return []
    
    def is_available(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama not available: {e}")
            return False
    
    def generate(self, prompt: str, model: str = None, stream: bool = False) -> str:
        """
        Generate text using Ollama.
        
        Args:
            prompt: The input prompt
            model: Optional model override
            stream: Whether to stream the response
        
        Returns:
            Generated text
        """
        model = model or self.model
        
        try:
            response = requests.post(
                self.api_endpoint,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=30000
            )
            response.raise_for_status()
            return response.json()['response'].strip()
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return ""
    
    def set_model(self, model: str):
        """Set the active model."""
        self.model = model
        logger.info(f"Model set to: {model}")


def think_prepare_implement(prompt: str, model: str = None, client: OllamaClient = None) -> Dict[str, str]:
    """
    Execute the think-prepare-implement workflow.
    
    Returns:
        Dictionary with 'thinking', 'plan', and 'implementation' keys
    """
    if client is None:
        client = OllamaClient()
    
    model = model or client.model
    
    # Step 1: Think (analyze and understand)
    think_prompt = f"""Analyze this request and break down what needs to be done:
{prompt}

Provide a clear analysis in 2-3 sentences."""
    
    thinking = client.generate(think_prompt, model)
    logger.info(f"💭 Thinking: {thinking[:100]}...")
    
    # Step 2: Prepare (plan the implementation)
    prepare_prompt = f"""Based on this analysis:
{thinking}

Create a detailed step-by-step plan to execute this request. Be specific and actionable."""
    
    plan = client.generate(prepare_prompt, model)
    logger.info(f"📋 Plan: {plan[:100]}...")
    
    # Step 3: Implement (execute)
    implement_prompt = f"""Following this plan:
{plan}

Now provide the implementation code, commands, or detailed steps to execute this. Be thorough and production-ready."""
    
    implementation = client.generate(implement_prompt, model)
    logger.info(f"✅ Implementation: {implementation[:100]}...")
    
    return {
        "thinking": thinking,
        "plan": plan,
        "implementation": implementation
    }
