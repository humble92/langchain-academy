# Module 1 Studio - LangGraph Execution Guide

This directory contains 3 graphs that can be run in LangGraph Studio:

## Included Graphs

1. **simple_graph** (`simple.py`) - Basic state graph example
2. **router** (`router.py`) - Router graph with tools
3. **agent** (`agent.py`) - Agent using calculation tools

## Setup Before Running

### 1. Environment Variable Configuration

Create a `.env` file in this directory and add the following content:

```bash
# OpenAI API Key (required - used by agent.py and router.py)
OPENAI_API_KEY=your_openai_api_key_here

# LangChain settings (optional)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langchain_api_key_here
LANGCHAIN_PROJECT=module-1-studio
```

### 2. Install Dependencies

Run the following command from the project root:

```bash
pip install -r module-1/studio/requirements.txt
```

## How to Run

### Using VS Code Debugger

1. Create `launch.json` with:
```
    "configurations": [
        {
            "name": "🚀 Debug Module-1 Studio",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/.venv/Scripts/langgraph.exe",
            "args": ["dev", "--allow-blocking"],
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}/module-1/studio",
            "env": {
                "PYTHONPATH": "${workspaceFolder}/module-1/studio",
                "OPENAI_API_KEY": "${env:OPENAI_API_KEY}",
                "BG_JOB_ISOLATED_LOOPS": "true"
            },
            "justMyCode": false
        }
    ]
```
2. In VS Code, press `Ctrl+Shift+P` and select "Debug: Select and Start Debugging"
3. Select "🚀 Debug Module-1 Studio"

### Direct Terminal Execution

```bash
cd module-1/studio
langgraph dev --allow-blocking
```

> 💡 The `--allow-blocking` flag prevents synchronous blocking call errors during development.

## Testing Graphs

Once the server is running, open your browser and go to `https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024` to test the graphs in LangGraph Studio.

### simple_graph
- Input: `{"graph_state": "Hi"}`
- Output: Randomly "Hi I am happy!" or "Hi I am sad!"

### router
- Input in message format (e.g., "What is 5 times 3?")
- Performs calculations using the multiply tool

### agent  
- Input in message format (e.g., "Calculate (10 + 5) * 2")
- Performs complex calculations using add, multiply, and divide tools 