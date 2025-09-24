from langchain_openai import OpenAI
from langgraph.graph import StateGraph
import os
from typing import Optional, TypedDict, List
from openai import OpenAI as OpenAIAPI  # added for embeddings

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
        # LangChain LLM for text generation
        self.llm = OpenAI(api_key=api_key)
        # Raw OpenAI client reused for embeddings (no re-auth each call)
        self._raw = OpenAIAPI(api_key=api_key)

    def run_prompt(self, prompt: str) -> str:
        response = self.llm(prompt)
        return response

    def embed_prompt(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """
        Return embedding vector for supplied text using the shared API client.
        """
        resp = self._raw.embeddings.create(model=model, input=text)
        return resp.data[0]

    def run_prompt_with_embedding(self, prompt: str) -> dict:
        """
        Convenience: generate embedding for prompt and also return original text.
        """
        emb = self.embed_prompt(prompt).embedding
        return {
            "prompt": prompt,
            "embedding_dimensions": len(emb),
            "embedding": emb,
        }

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
    # Embedding usage
    emb = client.embed_prompt("Architecture Decision Records automation")
    print(emb)

    result = client.run_prompt_with_embedding("ADR automation agent design considerations")
    print(f"Combined embedding dims: {result['embedding_dimensions']}")

    graph = client.build_graph()
    # Demo invocation of compiled graph
    print(graph.invoke({"input": "Test graph state"}))
