from langchain_openai import OpenAI
from langgraph.graph import StateGraph
import os
from typing import Optional, TypedDict, List, Dict, Any
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

        # --- Chroma vector store setup (lazy) ---
        self._chroma_client = None
        self._chroma_collection = None
        self._chroma_path = os.getenv("ADR_VECTOR_STORE_PATH", ".chroma")
        self._chroma_collection_name = os.getenv("ADR_VECTOR_COLLECTION", "adr_embeddings")

    # ---------------- Embeddings ----------------
    def embed_prompt(self, text: str, model: str = "text-embedding-3-small") -> Any:
        """
        Return embedding vector for supplied text using the shared API client.
        """
        resp = self._raw.embeddings.create(model=model, input=text)
        return resp.data[0]  # keep legacy object return

    def embed_text_vector(self, text: str, model: str = "text-embedding-3-small") -> List[float]:
        """
        New: directly return embedding vector (list[float]) for easier downstream usage.
        """
        resp = self._raw.embeddings.create(model=model, input=text)
        return resp.data[0].embedding

    def run_prompt_with_embedding(self, prompt: str) -> dict:
        """
        Convenience: generate embedding for prompt and also return original text.
        """
        emb = self.embed_text_vector(prompt)
        return {
            "prompt": prompt,
            "embedding_dimensions": len(emb),
            "embedding": emb,
        }

    # ---------------- Chroma Integration ----------------
    def _ensure_chroma(self):
        if self._chroma_client and self._chroma_collection:
            return
        try:
            import chromadb  # local import to allow optional dependency
        except ImportError as e:
            raise RuntimeError("chromadb not installed. Install with: pip install chromadb") from e

        self._chroma_client = chromadb.PersistentClient(path=self._chroma_path)
        self._chroma_collection = self._chroma_client.get_or_create_collection(
            name=self._chroma_collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_adr_text(self, doc_id: str, text: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Store ADR (or related content) embedding in Chroma.
        If same id exists, it will be upserted by deleting then adding.
        """
        self._ensure_chroma()
        vec = self.embed_text_vector(text)
        # Simple upsert strategy
        try:
            self._chroma_collection.delete(ids=[doc_id])
        except Exception:
            pass  # ignore if not existing
        self._chroma_collection.add(
            ids=[doc_id],
            documents=[text],
            embeddings=[vec],
            metadatas=[metadata or {}]
        )

    def query_similar(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Semantic similarity search against stored ADR embeddings.
        """
        self._ensure_chroma()
        q_vec = self.embed_text_vector(query)
        res = self._chroma_collection.query(
            query_embeddings=[q_vec],
            n_results=top_k,
            include=["documents", "metadatas", "distances"]
        )
        # Normalize result list
        results = []
        for i in range(len(res["ids"][0])):
            results.append({
                "id": res["ids"][0][i],
                "document": res["documents"][0][i],
                "metadata": res["metadatas"][0][i],
                "distance": res["distances"][0][i],
            })
        return results

    # ---------------- Graph ----------------
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

    def run_prompt(self, prompt: str) -> str:
        response = self.llm(prompt)
        return response

if __name__ == "__main__":
    # Example usage relying on environment variable
    client = OpenAIClient()
    print(client.run_prompt("Hello, OpenAI!"))
    # Embedding usage
    emb_vec = client.embed_text_vector("Architecture Decision Records automation")
    print(f"Vector dims: {len(emb_vec)}")

    result = client.run_prompt_with_embedding("ADR automation agent design considerations")
    print(f"Combined embedding dims: {result['embedding_dimensions']}")

    # --- Chroma demo ---
    # client.add_adr_text(
    #     doc_id="adr-001",
    #     text="Decision: Adopt PostgreSQL for ADR metadata storage due to reliability and JSONB support.",
    #     metadata={"status": "Accepted", "category": "storage"}
    # )
    # client.add_adr_text(
    #     doc_id="adr-002",
    #     text="Decision: Use GitHub Actions to automate ADR validation and pull request workflows.",
    #     metadata={"status": "Proposed", "category": "automation"}
    # )
    client.add_adr_text(
        doc_id="diagram-001",
        text="",
        metadata={"status": "In progress", "category": "diagram"}
    )
    similar = client.query_similar("How do we store ADR metadata?", top_k=2)
    print("Similarity results:", similar)

    similar = client.query_similar("How the car is working", top_k=2)
    print("Similarity results for how car is working:", similar)

    graph = client.build_graph()
    # Demo invocation of compiled graph
    print(graph.invoke({"input": "Test graph state"}))
