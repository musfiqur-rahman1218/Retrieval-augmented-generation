📘 RAG-Based Q&A System – Chapter 2 (Rules of the Road)
📌 Project Overview

This project implements a Retrieval-Augmented Generation (RAG) system that allows users to ask questions about Chapter 2 – Rules of the Road (DH-Chapter2.pdf).

The system:

Extracts text from the PDF

Splits it into meaningful chunks

Converts chunks into vector embeddings using Jina Embeddings

Stores embeddings in ChromaDB (vector database)

Retrieves relevant chunks for a user question

Uses an OpenAI-compatible LLM (via OpenRouter) to generate an answer

Displays source page numbers for transparency

The system ensures answers are grounded in the provided document only.

🏗️ System Architecture
User Question
      ↓
Embedding (Jina)
      ↓
Vector Search (ChromaDB)
      ↓
Top Relevant Chunks
      ↓
LLM (OpenRouter / OpenAI-compatible)
      ↓
Grounded Answer + Source Pages
📂 Project Structure
Rag_assignment/
│
├── data/
│   ├── DH-Chapter2.pdf
│   └── chroma_db/        # Vector database (auto-generated)
│
├── main.py               # Main RAG application
├── requirement.txt       # Dependencies
├── .env                  # API keys (not committed)
└── README.md
⚙️ Technologies Used

Python

PyMuPDF (fitz) – PDF text extraction

LangChain – Chunking and vector store interface

Jina Embeddings API – Text embedding

ChromaDB – Vector database

OpenRouter (OpenAI-compatible API) – LLM for answer generation

🚀 Installation & Setup
1️⃣ Clone the Repository
git clone <your-repo-url>
cd Rag_assignment
2️⃣ Install Dependencies (using uv)
uv pip install -r requirement.txt
3️⃣ Add API Keys

Create a .env file in the root directory:

JINA_API_KEY=your_jina_api_key
OPENAI_API_KEY=your_openrouter_key
OPENAI_BASE_URL=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-4o-mini

⚠️ Never commit your .env file.

▶️ Running the Application
Step 1 (First time only): Build Vector Database

In main.py, set:

REBUILD_DB = True

Then run:

python main.py

After the database is built, set:

REBUILD_DB = False
Step 2: Run the RAG Chat System
python main.py

Example interaction:

You: What are the rules about parking and stopping?


Assistant:
You must obey signs restricting stopping or parking...
...


Sources (pages): [25]
🧠 How It Works
1️⃣ Text Extraction

The system uses PyMuPDF to extract text page by page from the PDF.
If a page has poor extraction, a fallback block-based extraction method is used.

2️⃣ Chunking

The text is split into smaller segments using:

chunk_size = 800

chunk_overlap = 150

This ensures:

Better retrieval accuracy

Context preservation between chunks

3️⃣ Embeddings

Each chunk is converted into a vector using:

Jina Embeddings (jina-embeddings-v2-base-en)

These vectors represent semantic meaning of the text.

4️⃣ Vector Storage (ChromaDB)

The embeddings are stored in a local persistent Chroma database:

data/chroma_db/

Chroma enables similarity search between:

User question vector

Stored chunk vectors

5️⃣ Retrieval

When a user asks a question:

retrieved = vectordb.similarity_search(question, k=10)

The system:

Converts the question to an embedding

Finds the most similar chunks

Returns top relevant results

6️⃣ Generation (Grounded Answer)

The retrieved chunks are passed to the LLM with a strict instruction:

“Answer ONLY using the provided context. If not found, say you can't find it.”

This ensures:

No hallucination

Fully grounded answers

Transparent citations

🔍 Retrieval Strategy

The system uses similarity search with k=10 to ensure:

Higher recall for specific rules

Better coverage for detailed questions

Source page numbers are displayed to provide evidence.

✅ Example Questions

What are the rules about parking and stopping?

What is the crosswalk stopping distance rule?

What are traffic control signals?

What are the rules about backing?

📈 Strengths of This Implementation

✔ Grounded responses
✔ Transparent source citation
✔ Persistent vector database
✔ Clean modular code
✔ Interactive chat loop
✔ Adjustable retrieval depth

🛑 Limitations

Works only on Chapter 2 PDF

Requires internet connection (Jina + OpenRouter APIs)

Retrieval quality depends on chunk size and k value

🎓 Learning Outcomes

This project demonstrates:

Practical implementation of RAG architecture

Vector embeddings and semantic search

Vector database persistence

Prompt engineering for grounded responses

End-to-end LLM integration

👨‍💻 Author

Md. Musfiqur Rahman
MSc Computing & Data Analytics