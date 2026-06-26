# 🚀 Website RAG Platform

An AI-powered Retrieval-Augmented Generation (RAG) platform that transforms any website into a searchable knowledge base.

The platform crawls websites, indexes their content, performs keyword and semantic search, and generates grounded AI answers using Large Language Models (LLMs).

---

## ✨ Key Features

### 🌐 Intelligent Web Crawling
- Multithreaded crawler
- Domain-restricted crawling
- URL normalization
- Internal link discovery
- Crawl graph visualization

### 🔍 Search Engine
- TF-IDF ranking
- Exact phrase search
- Autocomplete suggestions
- Search analytics
- Pagination

### 🤖 AI Question Answering
- Semantic search with embeddings
- Vector similarity retrieval
- Retrieval-Augmented Generation (RAG)
- Groq LLM integration
- Source-aware responses

### 📚 Knowledge Base Generation
- Crawl any documentation website
- Automatic text chunking
- Embedding generation
- Dynamic indexing
- Reusable knowledge bases

### 🐳 Deployment
- Docker support
- Docker Compose
- Environment configuration
- Easy local setup

---

# 🏗️ System Architecture

```text
                  User
                    │
                    ▼
            Flask Web Interface
                    │
      ┌─────────────┴─────────────┐
      │                           │
      ▼                           ▼
 TF-IDF Search Engine         RAG Pipeline
      │                           │
      ▼                           ▼
 SQLite Database      Sentence Transformers
                                  │
                                  ▼
                          Vector Similarity Search
                                  │
                                  ▼
                              Groq LLM
                                  │
                                  ▼
                             AI Response
```

---

# ⚙️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Backend | Python, Flask |
| Database | SQLite |
| Search | TF-IDF, Inverted Index |
| AI | Sentence Transformers, Vector Embeddings, Groq API |
| Web Crawling | BeautifulSoup, Requests |
| Deployment | Docker, Docker Compose |
| Version Control | Git, GitHub |

---

# 📁 Project Structure

```text
website-rag-platform/
│
├── crawler/
│   ├── crawler.py
│   ├── fetcher.py
│   ├── parser.py
│   └── queue_manager.py
│
├── indexer/
│
├── rag/
│
├── frontend/
│
├── search/
│
├── database/
│
├── data/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 📸 Screenshots

## 🏠 Home Page

> Add screenshot

---

## 🔍 Search Results

> Add screenshot

---

## 🤖 AI Answer

> Add screenshot

---

## 📚 Knowledge Base Builder

> Add screenshot

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/devanupriyj-code/website-rag-platform.git

cd website-rag-platform
```

## Environment Variables

Create a `.env` file.

```env
GROQ_API_KEY=your_api_key
```

---

## Run with Docker

```bash
docker compose up --build
```

Visit

```
http://localhost:5000
```

---

## Local Development

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python -m frontend.app
```

---

# 🔄 Workflow

### 1️⃣ Crawl Website

The crawler visits pages, extracts content, and stores the information in SQLite.

↓

### 2️⃣ Build Search Index

TF-IDF indexing creates an inverted index for efficient keyword search.

↓

### 3️⃣ Generate Embeddings

Website content is split into chunks and converted into dense vector embeddings.

↓

### 4️⃣ Retrieve Relevant Context

The system performs:

- Keyword Search (TF-IDF)
- Semantic Search (Vector Similarity)

↓

### 5️⃣ Generate AI Answer

Retrieved chunks are sent to the Groq LLM, which generates a grounded answer based only on the retrieved context.

---

# 🌟 Highlights

- ✅ Built a search engine from scratch
- ✅ Multithreaded web crawler
- ✅ Dynamic website indexing
- ✅ Semantic search using embeddings
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ Dockerized deployment
- ✅ Modular architecture

---

# 🚀 Future Improvements

- BM25 ranking
- Redis caching
- PostgreSQL support
- Multiple knowledge bases
- Citation links
- Authentication
- Dark mode
- Incremental crawling
- Hybrid search (TF-IDF + Vector)

---

# 📊 Why This Project?

Traditional search engines return documents.

This platform retrieves the most relevant website content and uses Retrieval-Augmented Generation (RAG) to generate context-aware, explainable answers while reducing hallucinations.

---

# 👨‍💻 Author

**Devanupriy Jain**

First-Year B.Tech CSE Student

Interested in:
- Search Systems
- Artificial Intelligence
- Backend Development
- Information Retrieval
- Open Source

---

⭐ If you found this project useful, consider giving it a star!
