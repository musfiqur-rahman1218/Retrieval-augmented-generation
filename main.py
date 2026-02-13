import os
import fitz
import requests
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

from openai import OpenAI

PDF_PATH = "data\DH-Chapter2(1).pdf"
CHROMA_DIR = "data\chroma_db"

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# --- Jina Embeddings wrapper (simple) ---
class JinaEmbeddings:
    def __init__(self, api_key: str, model: str = "jina-embeddings-v2-base-en"):
        if not api_key:
            raise ValueError("Missing JINA_API_KEY. Put it in a .env file.")
        self.api_key = api_key
        self.model = model
        self.url = "https://api.jina.ai/v1/embeddings"

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {"model": self.model, "input": texts}
        r = requests.post(self.url, headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        data = r.json()["data"]
        return [item["embedding"] for item in data]

    def embed_query(self, text: str) -> list[float]:
        return self.embed_documents([text])[0]

def build_context(docs: list[Document]) -> str:
    """Join retrieved chunks into a single context string with page markers."""
    parts = []
    for d in docs:
        page = d.metadata.get("page", "?")
        parts.append(f"[Page {page}] {d.page_content}")
    return "\n\n".join(parts)

def generate_answer(question: str, context: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY. Put it in a .env file.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
You are a helpful assistant. Answer the user's question ONLY using the provided context.
If the answer is not in the context, say: "I can't find that in Chapter 2."

Context:
{context}

Question:
{question}

Answer in a clear, short way.
"""

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You answer strictly from the given context."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return resp.choices[0].message.content.strip()

if __name__ == "__main__":
    embeddings = JinaEmbeddings(JINA_API_KEY)

    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    print("\n✅ RAG is ready. Type a question (or type 'exit' to quit).\n")

while True:
    question = input("You: ").strip()
    if not question:
        continue
    if question.lower() in {"exit", "quit"}:
        print("Bye 👋")
        break

    retrieved = vectordb.max_marginal_relevance_search(
    question,
    k=6,          # how many chunks you finally use
    fetch_k=20    # how many it considers first
)

    # Optional: de-dup similar results (helps avoid repeats)
    seen = set()
    unique = []
    for d in retrieved:
        key = (d.metadata.get("page"), d.page_content[:120])
        if key not in seen:
            seen.add(key)
            unique.append(d)

    context = build_context(unique)
    answer = generate_answer(question, context)

    pages = sorted({d.metadata.get("page") for d in unique})

    print("\nAssistant:\n", answer)
    print("\nSources (pages):", pages)
    print("\n" + "-" * 60 + "\n")