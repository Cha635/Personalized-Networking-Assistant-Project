import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()

# Model names used by Hugging Face pipelines
MODEL_NAMES = {
    "event_analysis": os.getenv("EVENT_ANALYSIS_MODEL", "typeform/distilbert-base-uncased-mnli"),
    "text_generator": os.getenv("TEXT_GENERATOR_MODEL", "gpt2"),
}

# Wikipedia REST API base URL (no auth required)
FACT_CHECK_API = os.getenv(
    "FACT_CHECK_API",
    "https://en.wikipedia.org/api/rest_v1/page/summary"
)

# FastAPI backend URL (used by Streamlit frontend)
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Google Gemini API Key (Reserved for future Google Gemini integration)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
