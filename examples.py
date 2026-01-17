#!/usr/bin/env python3
"""
Example usage of CLIAgent programmatically
Shows how to use the agent without the CLI
"""

from agent import Agent
import json

def example_1_basic_task():
    """Example 1: Execute a basic task"""
    print("\n" + "="*60)
    print("Example 1: Basic Task Execution")
    print("="*60 + "\n")
    
    agent = Agent()
    
    # Check if Ollama is available
    if not agent.client.is_available():
        print("❌ Ollama is not running. Start it with: ollama serve")
        return
    
    result = agent.execute("Create a Python function that checks if a string is a palindrome")
    
    if "implementation" in result:
        print("Generated code:")
        print(result["implementation"])


def example_2_file_operations():
    """Example 2: File creation and management"""
    print("\n" + "="*60)
    print("Example 2: File Operations")
    print("="*60 + "\n")
    
    agent = Agent()
    
    # Create a file
    agent.create_file(
        "example_script.py",
        "print('Hello from CLIAgent!')\nprint('This file was created by the agent')"
    )
    
    # Read it back
    content = agent.read_file("example_script.py")
    print("File content:")
    print(content)
    
    # List files
    files = agent.list_files(".")
    print("\nFiles in directory:")
    for f in files[:5]:  # Show first 5
        print(f"  - {f}")


def example_3_model_switching():
    """Example 3: List and switch models"""
    print("\n" + "="*60)
    print("Example 3: Model Management")
    print("="*60 + "\n")
    
    agent = Agent()
    
    models = agent.get_available_models()
    print(f"Available models ({len(models)} total):")
    for model in models:
        print(f"  • {model}")
    
    if models:
        print(f"\nCurrent model: {agent.client.model}")
        print(f"Switching to: {models[0]}")
        agent.set_model(models[0])


def example_4_session_persistence():
    """Example 4: Session state persistence"""
    print("\n" + "="*60)
    print("Example 4: Session Persistence")
    print("="*60 + "\n")
    
    agent = Agent()
    
    print("Current session state:")
    state = agent.session_state
    print(f"  Messages: {len(state['messages'])}")
    print(f"  Files created: {len(state['files_created'])}")
    print(f"  Files modified: {len(state['files_modified'])}")
    
    print(f"\nSession file: {agent.client.config.session_file}")


def example_5_web_access():
    """Example 5: Web access capabilities"""
    print("\n" + "="*60)
    print("Example 5: Web Access")
    print("="*60 + "\n")
    
    agent = Agent()
    
    # Note: This requires internet connection
    print("Web access is available through:")
    print("  • agent.fetch_web(url) - Fetch a specific URL")
    print("  • agent.search_web(query) - Search the internet")
    
    print("\nExample: Fetching GitHub homepage")
    content = agent.fetch_web("https://github.com")
    if content:
        print(f"✅ Successfully fetched {len(content)} bytes")
        print(f"First 200 chars: {content[:200]}...")
    else:
        print("❌ Failed to fetch (no internet or blocked)")


def show_agent_capabilities():
    """Display all agent capabilities"""
    print("\n" + "="*60)
    print("CLIAgent Capabilities")
    print("="*60 + "\n")
    
    capabilities = {
        "LLM Integration": [
            "• Multiple Ollama models support",
            "• Think-Prepare-Implement workflow",
            "• Custom prompts",
            "• Model switching"
        ],
        "File Management": [
            "• Create files",
            "• Edit/append content",
            "• Read files",
            "• Delete files",
            "• List directories"
        ],
        "Web Access": [
            "• Fetch web pages",
            "• Search the internet",
            "• Parse HTML content"
        ],
        "Session Management": [
            "• Automatic state persistence",
            "• Conversation history",
            "• File tracking",
            "• Timestamped sessions"
        ]
    }
    
    for category, items in capabilities.items():
        print(f"{category}:")
        for item in items:
            print(f"  {item}")
        print()


if __name__ == "__main__":
    import sys
    
    print("\n" + "🤖 CLIAgent Examples" + "\n")
    
    examples = {
        "1": ("Basic Task", example_1_basic_task),
        "2": ("File Operations", example_2_file_operations),
        "3": ("Model Management", example_3_model_switching),
        "4": ("Session Persistence", example_4_session_persistence),
        "5": ("Web Access", example_5_web_access),
        "6": ("Capabilities", show_agent_capabilities),
        "all": ("Run All Examples", None)
    }
    
    print("Available examples:")
    for key, (desc, _) in examples.items():
        print(f"  {key}. {desc}")
    print("\nUsage: python examples.py [1-6|all]")
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        
        if choice == "all":
            example_1_basic_task()
            example_2_file_operations()
            example_3_model_switching()
            example_4_session_persistence()
            example_5_web_access()
        elif choice in examples and examples[choice][1]:
            examples[choice][1]()
        else:
            print("Invalid choice")
    else:
        show_agent_capabilities()
