# 🤝 Personalized Networking Assistant

An AI-powered web application that generates smart, tailored conversation starters for professional and social networking events.  
Built with **FastAPI**, **Streamlit**, **DistilBERT** (zero-shot classification), and **GPT-2** (text generation), with real-time fact-checking via the **Wikipedia API**.

---

## 📌 Table of Contents

1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Tech Stack](#tech-stack)  
4. [Architecture](#architecture)  
5. [Directory Structure](#directory-structure)  
6. [Prerequisites](#prerequisites)  
7. [Installation & Setup](#installation--setup)  
8. [Running the Application](#running-the-application)  
9. [API Endpoints](#api-endpoints)  
10. [Running Tests](#running-tests)  
11. [Dataset](#dataset)  
12. [ER Diagram Overview](#er-diagram-overview)  
13. [Environment Variables](#environment-variables)  
14. [Ethical AI Considerations](#ethical-ai-considerations)  
15. [Future Improvements](#future-improvements)  

---

## Project Overview

The **Personalized Networking Assistant** helps users prepare for networking events by:

- Extracting key **themes** from an event description using DistilBERT zero-shot classification.  
- Generating 2–3 natural, context-aware **conversation starters** using GPT-2.  
- Providing **instant fact-checks** on any topic via the Wikipedia REST API (no API key required).  
- Logging **conversation history** and capturing **user feedback** (👍 / 👎) for continuous improvement.

---

## Features

| Feature | Description |
|---|---|
| 🎯 Theme Extraction | DistilBERT zero-shot classifier identifies top-3 themes from any event description |
| 💬 Conversation Generation | GPT-2 Small produces human-like, contextually relevant conversation starters |
| 🔎 Fact-Check | Wikipedia REST API returns a concise summary for any query |
| 📖 History | Last 5 sessions displayed with all starters and metadata |
| 📊 Feedback Log | Thumbs-up / thumbs-down ratings stored with timestamps and metrics |
| 🌐 Light UI | Clean Streamlit frontend with Inter font, gradient header, and card layout |
| 🧪 Unit & Integration Tests | Pytest suite covering all service modules and FastAPI routes |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit 1.45 |
| **Backend API** | FastAPI 0.115 + Uvicorn |
| **Theme Extraction** | DistilBERT (`typeform/distilbert-base-uncased-mnli`) via Hugging Face Transformers |
| **Text Generation** | GPT-2 Small via Hugging Face Transformers |
| **Fact-Checking** | Wikipedia REST API (no auth) |
| **Data Validation** | Pydantic v2 |
| **Data Persistence** | Local JSON files (`data/history.json`, `data/feedback.json`) |
| **Testing** | Pytest + FastAPI TestClient (httpx) |
| **Env Management** | python-dotenv |

---

## Architecture

```
┌─────────────────────────────────────────────┐
│          User (Browser: localhost:8501)      │
└───────────────────┬─────────────────────────┘
                    │  HTTP
┌───────────────────▼─────────────────────────┐
│         Streamlit Frontend (frontend/)       │
│  • Input form (event + interests)           │
│  • Generate / Fact-check / History buttons  │
│  • Feedback logging (like / dislike)        │
└───────────────────┬─────────────────────────┘
                    │  HTTP/JSON
┌───────────────────▼─────────────────────────┐
│      FastAPI Backend (app/)  :8000          │
│  POST /generate-conversation                │
│  POST /analyze-event                        │
│  POST /fact-check                           │
└──────┬──────────────┬──────────────┬────────┘
       │              │              │
┌──────▼──────┐ ┌─────▼──────┐ ┌────▼──────────┐
│DistilBERT   │ │  GPT-2     │ │Wikipedia REST │
│Zero-Shot    │ │ Generator  │ │    API        │
│Classifier   │ │            │ │               │
└─────────────┘ └────────────┘ └───────────────┘
                    │
          ┌─────────▼──────────┐
          │  data/ (JSON files) │
          │  history.json       │
          │  feedback.json      │
          └─────────────────────┘
```

---

## Directory Structure

```
Project/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Model names, API URLs, env vars
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py           # Pydantic request/response models
│   ├── routers/
│   │   ├── __init__.py
│   │   └── conversation.py      # API route handlers
│   └── services/
│       ├── __init__.py
│       ├── event_analyzer.py    # DistilBERT zero-shot theme extraction
│       ├── topic_generator.py   # GPT-2 conversation-starter generation
│       ├── fact_checker.py      # Wikipedia API fact-check
│       ├── history_logger.py    # Persist sessions → data/history.json
│       └── feedback_logger.py   # Persist ratings  → data/feedback.json
├── frontend/
│   └── streamlit_app.py         # Streamlit UI (light theme)
├── tests/
│   ├── conftest.py
│   ├── test_event_analyzer.py
│   ├── test_topic_generator.py
│   ├── test_fact_checker.py
│   └── test_routes.py
├── data/
│   ├── networking_events_dataset.json  # 8 sample networking events
│   ├── history.json                    # Auto-generated at runtime
│   └── feedback.json                   # Auto-generated at runtime
├── .env                         # Local env vars (not committed)
├── .env.example                 # Template – copy to .env
├── requirements.txt
└── README.md
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.10 or higher |
| pip | Latest |
| Git | Any recent version |
| Internet | Required (model download + Wikipedia API) |
| RAM | Minimum 4 GB (8 GB recommended) |

> **Note:** Both DistilBERT and GPT-2 models are downloaded automatically from Hugging Face on first run and cached locally (~500 MB total). Subsequent starts are fast.

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/personalized-networking-assistant.git
cd personalized-networking-assistant
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
# Copy the template
cp .env.example .env
```

Open `.env` and (optionally) add your **Google Gemini API key** if you want to use Gemini features in the future:

```
GEMINI_API_KEY=your_key_here
```

All other values have sensible defaults and work out of the box.

---

## Running the Application

You need **two terminal windows** running simultaneously.

### Terminal 1 – FastAPI Backend

```bash
# From the project root (where app/ lives)
uvicorn app.main:app --reload
```

The API will be available at:  
- **Base URL:** `http://127.0.0.1:8000`  
- **Interactive Docs (Swagger UI):** `http://127.0.0.1:8000/docs`  
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Terminal 2 – Streamlit Frontend

```bash
# From the project root
streamlit run frontend/streamlit_app.py
```

Open your browser at **`http://localhost:8501`**.

> ⚠️ **First run:** Hugging Face will download DistilBERT (~265 MB) and GPT-2 (~500 MB) on first startup. This can take several minutes depending on your connection speed. Subsequent starts use the local cache.

---

## API Endpoints

All endpoints accept and return JSON.

### `POST /generate-conversation`

Generate conversation starters for a networking event.

**Request body:**
```json
{
  "description": "AI for Sustainable Cities",
  "interests": ["climate change", "urban planning"]
}
```

**Response:**
```json
{
  "topics": ["AI", "sustainability", "urban planning"],
  "suggestions": [
    "How do you think AI-driven traffic optimization could realistically cut emissions?",
    "Which city do you think leads in sustainable AI deployment?"
  ]
}
```

---

### `POST /analyze-event`

Extract themes only (without generating starters).

**Request body:**
```json
{ "description": "Blockchain in healthcare and supply chains" }
```

**Response:**
```json
{ "topics": ["blockchain", "healthcare", "data science"] }
```

---

### `POST /fact-check`

Return a Wikipedia summary for a given query.

**Request body:**
```json
{ "query": "blockchain in healthcare" }
```

**Response:**
```json
{ "summary": "Blockchain is a system of recording information in a way that makes it difficult or impossible to change, hack, or cheat the system..." }
```

---

## Running Tests

```bash
# Run all tests from the project root
pytest tests/ -v

# With coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

### Test coverage

| Test File | What it covers |
|---|---|
| `test_event_analyzer.py` | DistilBERT output structure (type, length, label membership) |
| `test_topic_generator.py` | GPT-2 output structure (type, length, non-blank strings) |
| `test_fact_checker.py` | Wikipedia service (happy path, missing data, mocked errors) |
| `test_routes.py` | FastAPI endpoints (200 responses, 422 validation, root health-check) |

---

## Dataset

`data/networking_events_dataset.json` contains **8 curated sample networking events** spanning:

| # | Event | Themes |
|---|---|---|
| 1 | AI for Sustainable Cities | AI, sustainability, urban planning |
| 2 | HealthTech Innovation Summit | healthcare, AI, biotech |
| 3 | Blockchain & DeFi Forum | blockchain, finance, cybersecurity |
| 4 | EdTech & Future of Learning | education, AI, entrepreneurship |
| 5 | Robotics & Automation Expo | robotics, AI, data science |
| 6 | Cybersecurity & Zero-Trust Summit | cybersecurity, AI, blockchain |
| 7 | Climate Tech & Clean Energy Forum | sustainability, climate change, finance |
| 8 | Data Science & Analytics World | data science, AI, entrepreneurship |

Each entry includes the event description, extracted themes, sample user interests, and example conversation starters for reference.  
The sidebar in the Streamlit UI displays these events for quick copy-paste inspiration.

---

## ER Diagram Overview

The data model has six entities:

```
USER_PROFILE ──< NETWORKING_SESSION >── EVENT_CONTEXT
                       │
           ┌───────────┼───────────┐
           ▼           ▼           ▼
  GENERATED_STARTER  WIKIPEDIA   LOG_ENTRY
                    _FACT_CHECK
```

| Entity | Primary Key | Key Attributes |
|---|---|---|
| USER_PROFILE | UserID | BioText, currentEventCache |
| EVENT_CONTEXT | EventID | EventDescription, AnalyzedThemes |
| NETWORKING_SESSION | SessionID | UserID (FK), EventID (FK), SessionTimestamp |
| GENERATED_STARTER | StarterID | SessionID (FK), StarterText, ContextPromptUsed |
| WIKIPEDIA_FACT_CHECK | FactCheckID | SessionID (FK), VerifiedQueryText, WikipediaSourceURL |
| LOG_ENTRY | LogID | SessionID (FK), ActionType, PayloadJSON, Timestamp |

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `EVENT_ANALYSIS_MODEL` | `typeform/distilbert-base-uncased-mnli` | Hugging Face model for zero-shot classification |
| `TEXT_GENERATOR_MODEL` | `gpt2` | Hugging Face model for text generation |
| `FACT_CHECK_API` | `https://en.wikipedia.org/api/rest_v1/page/summary` | Wikipedia REST API base URL |
| `BACKEND_URL` | `http://127.0.0.1:8000` | FastAPI server URL consumed by Streamlit |
| `GEMINI_API_KEY` | *(empty)* | Google Gemini API key (optional, future use) |

Copy `.env.example` to `.env` and fill in any values you wish to override.

---

## Ethical AI Considerations

- **Transparency:** Generated conversation starters are clearly labeled as AI-generated suggestions, not facts.  
- **Bias Awareness:** GPT-2 may produce biased or culturally insensitive outputs. Users are encouraged to review and edit suggestions before use.  
- **Data Privacy:** All user data (history and feedback) is stored **locally** in JSON files and never transmitted to external services.  
- **Fact-Checking Disclaimer:** Wikipedia summaries are useful starting points but may not always be accurate or up to date. Critical claims should be verified with authoritative sources.  
- **No PII Collection:** The application does not collect personally identifiable information.

---

## Future Improvements

- [ ] Replace local JSON storage with SQLite / PostgreSQL for multi-user support  
- [ ] Integrate **Google Gemini** for higher-quality conversation generation  
- [ ] Add user authentication (OAuth2 / JWT)  
- [ ] Implement vector search for similar past sessions (ChromaDB / FAISS)  
- [ ] Add a recommendation engine that learns from feedback history  
- [ ] Deploy to **Google Cloud Run** or **Hugging Face Spaces**  
- [ ] Add multilingual support for non-English events  

---

## License

This project was built as part of the **Google Cloud Generative AI** internship program via Smartbridge.  

---

*Made with ❤️ using Streamlit, FastAPI, and Hugging Face Transformers.*
