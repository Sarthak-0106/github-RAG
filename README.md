# 🚀 GitHub Repo RAG (Codebase Q&A System)

A **Retrieval-Augmented Generation (RAG)** system that lets you **chat with any GitHub repository**.

This project clones a repo, parses its code using AST (Tree-sitter), creates embeddings, and enables **natural language Q&A over the codebase**.

---

## ✨ Features

* 🔍 Clone and analyze any public GitHub repository
* 🧠 AST-based code chunking (functions, classes) using Tree-sitter
* 📄 README-aware understanding for high-level questions
* 🧩 Semantic search with vector embeddings
* 💬 Ask questions like:

  * *"What does this project do?"*
  * *"Explain the main logic"*
  * *"How does vector_store.py work?"*

---

## 🏗️ Architecture

```
GitHub Repo
   ↓
Clone Repo (GitPython)
   ↓
Load Files (AST + fallback)
   ↓
Chunk Code (Tree-sitter)
   ↓
Embeddings (MiniLM)
   ↓
Vector DB (Chroma)
   ↓
Retriever (Top-K search)
   ↓
LLM (Llama 3.1 via HF Router)
   ↓
Answer
```

---

## 📁 Project Structure

```
.
├── repo_loader.py     # Clone + load + AST parsing
├── vector_store.py    # Chunking + embeddings + DB
├── rag_chain.py       # LLM + retrieval chain
├── main.py            # Entry point (CLI app)
├── config.py          # API keys
└── chroma_db/         # Persistent vector storage
```

---

## ⚙️ Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd github-rag
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set API Key

In `config.py`:

```python
HF_TOKEN = "your_huggingface_api_key" 
should be in env file
```

---

## ▶️ Usage

Run the app:

```bash
python main.py
```

Enter a GitHub repo URL:

```
https://github.com/user/repo
```

Then start asking questions:

```
Ask a question: What is this project about?
Ask a question: Explain repo_loader.py
```

---

## 🧠 How It Works

### 1. Code Parsing (Tree-sitter)

* Extracts:

  * functions
  * classes
  * methods

### 2. Smart Chunking

* Each function/class becomes a semantic chunk
* Avoids random text splitting

### 3. Context Enrichment

* README is prioritized
* Repo structure is added as a summary document

### 4. Retrieval

* Top-K relevant chunks fetched
* Priority-based ranking

### 5. LLM Reasoning

* Uses Llama 3.1 (via HuggingFace router)
* Answers based on retrieved context

---

## ⚠️ Limitations

* ❌ Limited cross-file reasoning
* ❌ No dependency graph awareness
* ❌ May miss deeply nested logic

## 🛠️ Tech Stack

* Python
* LangChain
* Tree-sitter
* ChromaDB
* HuggingFace Embeddings
* Llama 3.1 (via HF Router)

---

## 💡 Example Questions

* What is this project about?
* How does the RAG pipeline work?
* Explain the vector store logic
* Where is the main entry point?

---

## 👨‍💻 Author

Built by Sarthak Raj

---

## ⭐ If You Like This Project

Give it a star ⭐ and share feedback!
