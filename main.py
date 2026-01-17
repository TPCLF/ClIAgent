#!/usr/bin/env python3
"""
CLIAgent - Terminal-based AI Coding Agent with Ollama LLM Integration
A clean, simple CLI for interacting with local LLMs for code generation and file manipulation.
"""

import click
import logging
import sys
from colorama import Fore, Back, Style, init
from agent import Agent
from config import config

# Initialize colorama for cross-platform colors
init(autoreset=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)


def print_header():
    """Print CLI header."""
    print(f"""{Fore.CYAN}
╔════════════════════════════════════════════════════════╗
║                    🤖 CLIAgent v1.0                    ║
║         Terminal AI Coding Agent with Ollama          ║
╚════════════════════════════════════════════════════════╝
{Style.RESET_ALL}""")


def print_success(msg: str):
    """Print success message."""
    print(f"{Fore.GREEN}✅ {msg}{Style.RESET_ALL}")


def print_error(msg: str):
    """Print error message."""
    print(f"{Fore.RED}❌ {msg}{Style.RESET_ALL}")


def print_info(msg: str):
    """Print info message."""
    print(f"{Fore.BLUE}ℹ️  {msg}{Style.RESET_ALL}")


@click.group()
def cli():
    """CLIAgent - AI Coding Agent CLI"""
    pass


@cli.command()
@click.option('--model', default=None, help='Model to use (default: mistral)')
@click.option('--workflow', is_flag=True, default=True, help='Use think-prepare-implement workflow')
@click.argument('prompt', required=True, nargs=-1)
def task(model, workflow, prompt):
    """Execute a task with the AI agent."""
    print_header()
    
    agent = Agent(model=model)
    
    # Check if Ollama is available
    if not agent.client.is_available():
        print_error("Ollama is not running. Start it with: ollama serve")
        return
    
    prompt_text = " ".join(prompt)
    print_info(f"Prompt: {prompt_text}\n")
    
    if model:
        print_info(f"Using model: {model}\n")
    
    result = agent.execute(prompt_text, use_workflow=workflow)
    
    if "error" in result:
        print_error(result["error"])
        return
    
    # Display results
    if "thinking" in result:
        print(f"\n{Fore.CYAN}💭 Thinking:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result['thinking']}{Style.RESET_ALL}\n")
    
    if "plan" in result:
        print(f"{Fore.CYAN}📋 Plan:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{result['plan']}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}✨ Implementation:{Style.RESET_ALL}")
    print(f"{Fore.WHITE}{result['implementation']}{Style.RESET_ALL}\n")
    
    print_success("Task completed. Session saved.")


@cli.command()
@click.option('--model', default=None, help='Model to use')
def interactive(model):
    """Start interactive session."""
    print_header()
    
    agent = Agent(model=model)
    
    if not agent.client.is_available():
        print_error("Ollama is not running. Start it with: ollama serve")
        return
    
    print(agent.show_status())
    print_info("Type 'exit' to quit, 'help' for commands\n")
    
    while True:
        try:
            # Use standard input for full line editing support (backspace works properly)
            sys.stdout.write(f"{Fore.YELLOW}➜ {Style.RESET_ALL}")
            sys.stdout.flush()
            user_input = sys.stdin.readline().strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print_success("Goodbye!")
                break
            
            if user_input.lower() == 'help':
                print_help_commands()
                continue
            
            if user_input.lower() == 'status':
                print(agent.show_status())
                continue
            
            if user_input.lower() == 'models':
                models = agent.get_available_models()
                print(f"Available models: {', '.join(models) if models else 'None'}\n")
                continue
            
            if user_input.startswith('model:'):
                model_name = user_input.replace('model:', '').strip()
                result = agent.set_model(model_name)
                print_info(result)
                continue
            
            if not user_input:
                continue
            
            print_info("Processing your request...")
            result = agent.execute(user_input)
            
            if "error" in result:
                print_error(result["error"])
                continue
            
            if "thinking" in result:
                print(f"\n{Fore.CYAN}💭 Thinking:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{result['thinking']}{Style.RESET_ALL}\n")
            
            if "plan" in result:
                print(f"{Fore.CYAN}📋 Plan:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{result['plan']}{Style.RESET_ALL}\n")
            
            if "implementation" in result:
                print(f"{Fore.CYAN}✨ Implementation:{Style.RESET_ALL}")
                print(f"{Fore.WHITE}{result['implementation']}{Style.RESET_ALL}\n")
                print_success("Task completed!")
        
        except KeyboardInterrupt:
            print_success("Session interrupted")
            break
        except Exception as e:
            print_error(f"Error: {e}")


@cli.command()
@click.option('--model', default=None, help='Model to use')
def models(model):
    """List available Ollama models."""
    print_header()
    
    agent = Agent(model=model)
    
    if not agent.client.is_available():
        print_error("Ollama is not running")
        return
    
    available = agent.get_available_models()
    
    if available:
        print(f"{Fore.CYAN}Available Models:{Style.RESET_ALL}")
        for i, m in enumerate(available, 1):
            print(f"  {i}. {Fore.GREEN}{m}{Style.RESET_ALL}")
    else:
        print_error("No models found")


@cli.command()
def status():
    """Show agent status."""
    print_header()
    agent = Agent()
    print(agent.show_status())


@cli.command()
@click.argument('filepath', required=True)
@click.argument('content', required=True)
@click.option('--overwrite', is_flag=True, help='Overwrite if exists')
def create(filepath, content, overwrite):
    """Create a file directly."""
    print_header()
    agent = Agent()
    
    if agent.create_file(filepath, content, overwrite):
        print_success(f"File created: {filepath}")
    else:
        print_error("Failed to create file")


def print_help_commands():
    """Print available commands in interactive mode."""
    help_text = f"""
{Fore.CYAN}Available Commands:{Style.RESET_ALL}
  help          - Show this help
  status        - Show agent status
  models        - List available models
  model:<name>  - Switch to a model
  exit/quit     - Exit the session
  <prompt>      - Execute a task with AI agent
"""
    print(help_text)


@cli.command()
def web():
    """Fetch and search the web (test)."""
    print_header()
    
    url = click.prompt("Enter URL to fetch")
    agent = Agent()
    
    content = agent.fetch_web(url)
    print(f"\n{Fore.CYAN}Content ({len(content)} chars):{Style.RESET_ALL}")
    print(content[:500] + "..." if len(content) > 500 else content)


if __name__ == '__main__':
    cli()
