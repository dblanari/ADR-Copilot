# src/README.md

## OpenAI Client Example

This module provides a simple Python client for connecting to OpenAI using LangChain and LangGraph.

### Features
- Connects to OpenAI via LangChain
- Runs prompts and returns responses
- Example method for building a LangGraph state graph

### Usage
```python
from client import OpenAIClient

client = OpenAIClient(api_key="your-openai-key")
response = client.run_prompt("Hello, OpenAI!")
print(response)

graph = client.build_graph()
# Add nodes and edges to the graph as needed
```

### Requirements
- `langchain_openai`
- `langgraph`

Install dependencies:
```bash
pip install langchain_openai langgraph
python3 -m pip install langchain_openai langgraph
```

### Run from Terminal

1. Run a Python file (example if you add a script named main.py):
```bash
python main.py
python client.py 
```
