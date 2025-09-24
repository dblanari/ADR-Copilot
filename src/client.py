from langchain_openai import OpenAI
from langgraph.graph import StateGraph
import os
from typing import Optional, TypedDict  # added TypedDict

class GraphState(TypedDict, total=False):  # added state schema
    input: str
    output: str

class OpenAIClient:
    def __init__(self, api_key: Optional[str] = None):  # changed from str | None
        # Fallback to environment variable if not explicitly provided
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set. Export it via: export OPENAI_API_KEY='your-openai-key'")
        self.api_key = api_key
        self.llm = OpenAI(api_key=api_key)

    def run_prompt(self, prompt: str) -> str:
        response = self.llm(prompt)
        return response

    def build_graph(self):
        # Provide required state_schema to StateGraph
        graph = StateGraph(GraphState)

        # Minimal node
        def echo(state: GraphState) -> GraphState:
            return {"output": state.get("input", "")}

        graph.add_node("echo", echo)
        graph.set_entry_point("echo")
        app = graph.compile()
        return app

if __name__ == "__main__":
    # Example usage relying on environment variable
    client = OpenAIClient()
    print(client.run_prompt("Hello, OpenAI!"))
    print(client.run_prompt("Generate small talk about AI."))
    graph = client.build_graph()
    # Demo invocation of compiled graph
    print(graph.invoke({"input": "Test graph state"}))
