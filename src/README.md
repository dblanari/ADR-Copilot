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

# ChromaDB Configuration Guide

ChromaDB is used as a vector database for storing and querying embeddings in this project.

## Installation

Install ChromaDB using pip:

```bash
pip install chromadb
```

## Basic Usage in This Project

The OpenAIClient class in `src/client.py` integrates ChromaDB for storing and searching embeddings. No manual setup is required beyond installation, but you can configure storage location and collection name using environment variables:

- `ADR_VECTOR_STORE_PATH`: Path to store ChromaDB data (default: `.chroma`)
- `ADR_VECTOR_COLLECTION`: Name of the ChromaDB collection (default: `adr_embeddings`)

Example:
```bash
export ADR_VECTOR_STORE_PATH="/path/to/chroma_store"
export ADR_VECTOR_COLLECTION="my_collection"
```

## Usage Example

After installing ChromaDB, you can use the vector store features via the OpenAIClient:

```python
from client import OpenAIClient
client = OpenAIClient()
client.add_adr_text(doc_id="adr-001", text="Example ADR text.")
similar = client.query_similar("Find similar ADRs", top_k=2)
print(similar)
```

## Troubleshooting
- If you see an error about `chromadb` not being installed, ensure you have run `pip install chromadb` in your environment.
- For advanced configuration, refer to the [ChromaDB documentation](https://docs.trychroma.com/).
