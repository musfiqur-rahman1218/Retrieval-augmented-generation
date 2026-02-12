import os
import fitz  # PyMuPDF
import requests
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma

PDF_PATH = "data\DH-Chapter2 (1).pdf"
CHROMA_DIR = "data\chroma_db"  # will be created locally

load_dotenv()
JINA_API_KEY = os.getenv("JINA_API_KEY")

def extract_pdf_text_by_page(pdf_path: str) -> list[dict]:
    doc = fitz.open(pdf_path)
    pages = []

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text")

        if len(text.strip()) < 200:
            blocks = page.get_text("blocks")
            text = " ".join((b[4] for b in blocks if isinstance(b[4], str)))

        text = " ".join(text.split())
        pages.append({"page": i + 1, "text": text})

    doc.close()
    return pages

def chunk_pages(pages: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = []

    for p in pages:
        if not p["text"]:
            continue
        split_texts = splitter.split_text(p["text"])
        for idx, t in enumerate(split_texts):
            # skip useless tiny chunks (like just headings)
            if len(t.strip()) < 80:
                continue
            chunks.append({"page": p["page"], "chunk_id": idx, "text": t})

    return chunks

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

if __name__ == "__main__":
    from langchain_community.vectorstores import Chroma

    embeddings = JinaEmbeddings(JINA_API_KEY)

    # Load existing DB instead of rebuilding
    vectordb = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    query = "What are the rules about parking and stopping?"
    results = vectordb.similarity_search(query, k=3)

    print("\n🔎 Query:", query)
    print("\nTop 3 Retrieved Chunks:\n")

    for i, doc in enumerate(results):
        print(f"Result {i+1}")
        print("Page:", doc.metadata["page"])
        print(doc.page_content[:500])
        print("-" * 50)