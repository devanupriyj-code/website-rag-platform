# 🚀 Website RAG Platform

An AI-powered search engine that can crawl websites, build a knowledge base, perform keyword and semantic search, and answer questions using Retrieval-Augmented Generation (RAG).

---

## ✨ Features

### 🌐 Web Crawling

* Multithreaded website crawler
* Dynamic domain-based crawling
* URL normalization
* Internal link discovery
* Crawl graph generation

### 🔍 Search Engine

* TF-IDF ranking
* Exact phrase search
* Autocomplete suggestions
* Search analytics
* Pagination support

### 🤖 AI-Powered Question Answering

* Semantic search using embeddings
* Vector similarity search
* Retrieval-Augmented Generation (RAG)
* Groq LLM integration
* Source-aware responses

### 📚 Knowledge Base Builder

* Crawl any documentation website
* Generate searchable knowledge bases
* Chunking and embedding generation
* Dynamic website indexing

### 🐳 Docker Support

* Dockerized application
* Docker Compose configuration
* Easy deployment and setup

---

## 🏗️ Architecture

```text
User
 │
 ▼
Flask Frontend
 │
 ├── TF-IDF Search Engine
 │        │
 │        ▼
 │    SQLite Database
 │
 └── RAG Pipeline
          │
          ▼
    Sentence Transformers
          │
          ▼
      Vector Search
          │
          ▼
       Groq LLM
          │
          ▼
       AI Answer
```

---

## 🛠️ Tech Stack

### Backend

* Python
* Flask
* SQLite

### Search

* TF-IDF Ranking
* Inverted Index
* Autocomplete Engine

### AI / RAG

* Sentence Transformers
* Vector Embeddings
* Groq API
* Semantic Retrieval

### Infrastructure

* Docker
* Docker Compose
* GitHub

---

## 📸 Screenshots

### Home Page

Add screenshot here

### Search Results

Add screenshot here

### AI Answer

Add screenshot here

### Knowledge Base Builder

Add screenshot here

---

## 🚀 Getting Started

### Clone Repository

```bash
git clone https://github.com/devanupriyj-code/website-rag-platform.git

cd website-rag-platform
```

### Create Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

### Run Using Docker

```bash
docker compose up --build
```

Open:

```text
http://localhost:5000
```

---

## 🔧 Local Development

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python -m frontend.app
```

---

## 📖 How It Works

### 1. Crawl Website

The crawler visits pages, extracts content, and stores information in SQLite.

### 2. Build Search Index

TF-IDF indexing generates an inverted index and IDF values.

### 3. Create Embeddings

Content is chunked and converted into vector embeddings.

### 4. Search

Users can search using:

* Keyword search (TF-IDF)
* Semantic search (embeddings)

### 5. AI Answers

Relevant chunks are retrieved and passed to a Groq LLM to generate grounded answers.

---

## 🎯 Future Improvements

* BM25 Ranking
* User Authentication
* Multiple Knowledge Bases
* Website Deployment
* Citation Links in AI Answers
* Dark Mode
* PostgreSQL Support
* Redis Caching

---

## 📈 Project Highlights

* Multithreaded crawler
* Search engine built from scratch
* Semantic search
* Retrieval-Augmented Generation (RAG)
* Dockerized deployment
* Dynamic website knowledge base generation

---

## 👨‍💻 Author

Devanupriy Jain

First-Year B.Tech CSE Student

Passionate about Search Systems, AI, Backend Development, and Open Source.
