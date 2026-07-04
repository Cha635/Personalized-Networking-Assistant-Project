"""
Integration tests for FastAPI API routes.

Uses FastAPI's built-in TestClient (wraps httpx) to exercise the full
request–response cycle without starting a real server.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ── Root health-check ─────────────────────────────────────────────────────────

def test_root_health_check():
    """GET / should return 200 and a welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


# ── /generate-conversation ─────────────────────────────────────────────────────

def test_generate_conversation_api():
    """Valid payload should return 200 with topics and suggestions."""
    payload = {
        "description": "Sustainability in smart cities",
        "interests": ["green energy", "public transport"]
    }
    response = client.post("/generate-conversation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert "suggestions" in data
    assert isinstance(data["topics"], list)
    assert isinstance(data["suggestions"], list)


def test_generate_conversation_returns_non_empty_suggestions():
    """Suggestions list must not be empty for a valid request."""
    payload = {
        "description": "AI in healthcare",
        "interests": ["diagnostics", "ethics"]
    }
    response = client.post("/generate-conversation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["suggestions"]) >= 1


def test_generate_conversation_invalid_request_422():
    """Missing required fields should trigger a 422 Unprocessable Entity."""
    response = client.post("/generate-conversation", json={})
    assert response.status_code == 422


def test_generate_conversation_missing_interests_422():
    """Sending only description (no interests) should trigger 422."""
    response = client.post("/generate-conversation", json={"description": "blockchain summit"})
    assert response.status_code == 422


# ── /analyze-event ─────────────────────────────────────────────────────────────

def test_analyze_event_api():
    """Valid description should return a topics list."""
    response = client.post("/analyze-event", json={"description": "blockchain in healthcare"})
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert isinstance(data["topics"], list)


def test_analyze_event_invalid_422():
    """Empty payload should return 422."""
    response = client.post("/analyze-event", json={})
    assert response.status_code == 422


# ── /fact-check ────────────────────────────────────────────────────────────────

def test_fact_check_api():
    """Valid query should return a summary string."""
    response = client.post("/fact-check", json={"query": "solar energy"})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data
    assert isinstance(data["summary"], str)


def test_fact_check_invalid_422():
    """Empty payload should return 422."""
    response = client.post("/fact-check", json={})
    assert response.status_code == 422
