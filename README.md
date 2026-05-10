# Veritas

An intelligent multi-agent research platform that performs automated research, claim extraction, contradiction detection, verification, and confidence scoring using a hybrid architecture combining LLM agents, semantic retrieval, and local ML models.

---

# 🚀 Overview

This project is an AI-powered research assistant system that:

- Breaks complex questions into research tasks
- Searches and analyzes sources
- Extracts structured factual claims
- Detects contradictions across sources
- Verifies evidence using hybrid ML + LLM reasoning
- Assigns confidence scores
- Generates explainable research reports

The system combines:
- Multi-agent orchestration
- Retrieval-augmented reasoning
- Semantic vector search
- Transformer-based stance classification
- Structured knowledge storage

---

# 🧠 Key Features

## ✅ Multi-Agent Architecture

Specialized agents collaborate to solve research tasks:

- **Planner Agent**
  - Breaks queries into sub-questions

- **Research Agent**
  - Retrieves and summarizes evidence

- **Claim Extraction Agent**
  - Converts text into structured factual claims

- **Verification Agent**
  - Evaluates evidence and claim validity

- **Writer Agent**
  - Synthesizes structured final reports

---

## 🔎 Semantic Knowledge Layer

Claims are stored in ChromaDB with embeddings for:

- Semantic retrieval
- Topic clustering
- Contradiction analysis
- Persistent research memory

---

## ⚖️ Contradiction Detection

The system identifies:
- Supporting claims
- Opposing claims
- Uncertain claims

using:
- Embedding similarity
- Transformer-based NLI models
- LLM reasoning

---

## 🧪 Hybrid ML + LLM Reasoning

The platform combines:
- Local transformer inference
- Embedding similarity scoring
- LLM-based nuanced reasoning

instead of relying entirely on LLM prompts.

---

## 📊 Explainable AI Pipeline

The system exposes:
- Agent execution traces
- Evidence sources
- Confidence reasoning
- Contradiction analysis

to improve transparency and interpretability.

---

# 🏗️ System Architecture

```text
Frontend (React / Next.js)
        ↓
FastAPI Backend
        ↓
Agent Orchestrator
        ↓
Agents:
  ├── Planner Agent
  ├── Research Agent
  ├── Claim Extraction Agent
  ├── Verification Agent
  └── Writer Agent
        ↓
ML Intelligence Layer
  ├── Embedding Similarity
  ├── Stance Classification
  └── Confidence Scoring
        ↓
ChromaDB Vector Store
        ↓
External Search + Scraping
```

---

# ⚙️ Tech Stack

## Backend
- Python
- FastAPI
- Google Agent Development Kit (ADK)

## Frontend
- React / Next.js

## AI / ML
- Gemini API
- Hugging Face Transformers
- PyTorch
- Sentence Transformers

## Vector Storage
- ChromaDB

## Search / Retrieval
- Tavily API
- BeautifulSoup
- newspaper3k

## Deployment
- Docker
- Docker Compose
- Nginx
- AWS EC2
- GitHub Actions CI/CD

---

# 🧩 Core Pipeline

## 1. Planning
The Planner Agent decomposes the user query into focused research tasks.

Example:
```json
{
  "tasks": [
    {
      "id": 1,
      "question": "What are the benefits of AI in software engineering?"
    },
    {
      "id": 2,
      "question": "What risks does AI introduce to software engineering jobs?"
    }
  ]
}
```

---

## 2. Research

The Research Agent:
- searches the web
- retrieves sources
- extracts relevant evidence

---

## 3. Claim Extraction

The Claim Extraction Agent converts evidence into structured claims.

Example:

```json
{
  "claim": "AI automation is reducing demand for junior software engineers.",
  "source_url": "...",
  "claim_type": "prediction"
}
```

---

## 4. Semantic Storage

Claims are embedded and stored in ChromaDB for:
- retrieval
- similarity search
- contradiction analysis

---

## 5. Verification + Contradiction Analysis

The system evaluates:
- supporting evidence
- contradicting evidence
- semantic consistency
- stance relationships

using:
- embedding similarity
- NLI transformers
- LLM reasoning

---

## 6. Final Synthesis

The Writer Agent generates:
- executive summaries
- key findings
- contradiction reports
- confidence explanations

---

# 🧠 ML Components

## Embedding Similarity

Used for:
- semantic retrieval
- claim clustering
- contradiction candidate filtering

Model:
```text
all-MiniLM-L6-v2
```

---

## Stance Classification

Used to determine whether evidence:
- supports
- opposes
- is neutral toward claims

Implemented using:
```text
DeBERTa / MNLI-based transformer models
```

---

# ⚡ Performance Optimizations

The system includes:

- Claim deduplication
- Topic clustering
- Batched embeddings
- Async research execution
- Multi-layer caching
- Similarity filtering before reasoning
- Reduced token usage via evidence snippets

---

# 🚀 Deployment

The backend is deployed using:

- Docker
- Docker Compose
- Nginx reverse proxy
- AWS EC2

CI/CD is automated via GitHub Actions.

Deployment flow:

```text
Push to GitHub
    ↓
GitHub Actions
    ↓
SSH into EC2
    ↓
Docker rebuild + restart
    ↓
Automatic deployment
```

---

# 🔐 Environment Variables

Example:

```env
GEMINI_API_KEY=
TAVILY_API_KEY=
CHROMA_DB_PATH=
```

---

# 🧪 Running Locally

## Backend

```bash
cd backend

pip install -r requirements.txt

uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

---

# 🐳 Docker

```bash
docker compose up --build
```

---

# 🎯 Example Query

```text
Will AI replace software engineers?
```

The system:
1. breaks the question into sub-questions
2. gathers evidence
3. extracts claims
4. retrieves semantically related claims
5. detects contradictions
6. classifies stance relationships
7. assigns confidence scores
8. generates a structured research report

---

# 📈 Future Improvements

Potential future features:

- Debate agents
- Persistent long-term memory
- Live collaborative research
- Streaming reasoning traces
- User-specific research profiles
- Autonomous follow-up questioning

---

# 📄 License

MIT License

---

# 👨‍💻 Author

Built as an experimental AI research and reasoning platform exploring:
- agentic systems
- retrieval-augmented generation
- structured AI reasoning
- hybrid ML + LLM architectures
