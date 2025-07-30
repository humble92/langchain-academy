#!/usr/bin/env python3
"""
Module 1 Studio Environment Setup Script
"""

import os
from pathlib import Path

def setup_env():
    """Setup environment file (.env)"""
    
    current_dir = Path(__file__).parent
    env_file = current_dir / ".env"
    
    if env_file.exists():
        print(f"✅ .env file already exists: {env_file}")
        return
    
    print("🔧 Starting Module 1 Studio environment setup...")
    print()
    
    # OpenAI API Key input
    openai_key = input("Enter your OpenAI API Key (required for agent.py and router.py): ").strip()
    
    # LangChain settings (optional)
    use_langchain = input("Do you want to use LangChain tracing? (y/n, default: n): ").strip().lower()
    
    langchain_key = ""
    if use_langchain in ['y', 'yes']:
        langchain_key = input("Enter your LangChain API Key (optional): ").strip()
    
    # Create .env file
    env_content = f"""# OpenAI API Key (required)
OPENAI_API_KEY={openai_key}

# LangChain settings (optional)
LANGCHAIN_TRACING_V2={'true' if use_langchain in ['y', 'yes'] else 'false'}
{f'LANGCHAIN_API_KEY={langchain_key}' if langchain_key else '# LANGCHAIN_API_KEY=your_langchain_api_key_here'}
LANGCHAIN_PROJECT=module-1-studio

# Other settings
PYTHONPATH=.
"""
    
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print(f"✅ .env file has been created: {env_file}")
        print()
        print("🚀 You can now run LangGraph Studio using:")
        print("   1. VS Code: Ctrl+Shift+P → Select '🚀 Debug Module-1 Studio'")
        print("   2. Terminal: cd module-1/studio && langgraph dev --allow-blocking")
        print()
        print("📋 Open your browser and go to https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024 to test the graphs!")
        print()
        print("💡 Note: The --allow-blocking flag prevents blocking call errors during development.")
        
    except Exception as e:
        print(f"❌ Error occurred while creating .env file: {e}")
        print("Please create the .env file manually.")

if __name__ == "__main__":
    setup_env() 