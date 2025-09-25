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

    def add_adr_file(self, doc_id: str, file: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Read ADR content from a file path and store embedding (wraps add_adr_text).
        Raises FileNotFoundError if file missing, ValueError if empty.
        """
        if not os.path.exists(file):
            raise FileNotFoundError(f"File not found: {file}")
        with open(file, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if not content:
            raise ValueError(f"File is empty: {file}")
        self.add_adr_text(doc_id=doc_id, text=content, metadata=metadata)

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
        print(f"Prompt length (chars): {len(prompt)}")
        try:
            response = self.llm(prompt)
            return response
        except Exception as e:
            print(f"Error in run_prompt: {e}")
            return f"Error: {e}"

    def summarize_text(self, text: str) -> str:
        """
        Summarize a document using the LLM. Returns a concise summary.
        """
        summary_prompt = f"Summarize the following document in 2-4 sentences for ADR generation, focusing on key decisions, context, and outcomes.\nDocument:\n{text}"
        return self.run_prompt(summary_prompt)

    def chunk_text(self, text: str, max_chars: int = 3000) -> List[str]:
        """
        Split text into chunks of max_chars length, preserving boundaries.
        """
        return [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

if __name__ == "__main__":
    client = OpenAIClient()
    # Embedding usage
    # emb_vec = client.embed_text_vector("Architecture Decision Records automation")
    # print(f"Vector dims: {len(emb_vec)}")

    # result = client.run_prompt_with_embedding("ADR automation agent design considerations")
    # print(f"Combined embedding dims: {result['embedding_dimensions']}")

    # client.add_adr_file(
    #     doc_id="Exploration_Document-001",
    #     file="/Users/denisblanari/work/code/ADR-Copilot/adr/adr-supporting/ADR003/Exploration_Document.md",
    #     metadata={"status": "completed", "category": "document"}
    # )
    #
    # client.add_adr_file(
    #     doc_id="diagram-001",
    #     file="/Users/denisblanari/work/code/ADR-Copilot/adr/adr-supporting/ADR003/diagram.puml",
    #     metadata={"status": "completed", "category": "diagram"}
    # )
    #
    # client.add_adr_file(
    #     doc_id="POC-001",
    #     file="/Users/denisblanari/work/code/ADR-Copilot/adr/adr-supporting/ADR003/Proof-of-Concept-Results.md",
    #     metadata={"status": "completed", "category": "document"}
    # )
    #
    # client.add_adr_file(
    #     doc_id="Notes-001",
    #     file="/Users/denisblanari/work/code/ADR-Copilot/adr/adr-supporting/ADR003/Meeting-Notes.md",
    #     metadata={"status": "completed", "category": "notes"}
    # )
    #
    # client.add_adr_file(
    #     doc_id="Standards-References-001",
    #     file="/Users/denisblanari/work/code/ADR-Copilot/adr/adr-supporting/ADR003/Example-Standards-References.txt",
    #     metadata={"status": "completed", "category": "document"}
    # )

    similar = client.query_similar("Payment Service notification Kafka", top_k=5)

    # Summarize each document before building documents_str
    summarized_docs = []
    for result in similar:
        summary = client.summarize_text(result['document'])
        summarized_docs.append(f"{result['id']}: {summary}")
    documents_str = "\n".join(summarized_docs)
    # print("Combined summarized documents:\n", documents_str)



    final_prompt = (
        "You are an expert software architect. Based on the provided supporting documentation, create a comprehensive Architecture Decision Record (ADR).\n"
        "Supporting documentation included:\n"
        # "Supporting documentation includes:\n"
        # "- Exploration documents\n"
        # "- Architecture diagrams\n"
        # "- Proof-of-Concept\n"
        # "- Meeting notes\n"
        # "- Standards references\n"
        # "Documents:\n"
        + documents_str
    )

    print("Final prompt for ADR:\n" + final_prompt)

    # Chunk the final prompt if too large
    # prompt_chunks = client.chunk_text(final_prompt, max_chars=3500)
    # adr_responses = []
    # for chunk in prompt_chunks:
    #     adr_responses.append(client.run_prompt(chunk))
    # print("\n -=- chunk -=- ".join(adr_responses))

    print("ADR Response:\n" + client.run_prompt(final_prompt))

    # graph = client.build_graph()
    # Demo invocation of compiled graph
    # print(graph.invoke({"input": "Test graph state"}))
