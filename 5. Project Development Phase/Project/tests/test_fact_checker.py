"""
Unit tests for fact_checker.fact_check.

External network calls are mocked via unittest.mock so that tests are fast,
hermetic, and suitable for CI environments without internet access.
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services import fact_checker


def _make_mock_response(extract: str, status_code: int = 200):
    """Helper: build a mock requests.Response object."""
    mock = MagicMock()
    mock.status_code = status_code
    mock.json.return_value = {"extract": extract, "title": "Test"}
    mock.raise_for_status.return_value = None
    return mock


# ── Happy-path test ────────────────────────────────────────────────────────────

def test_fact_checker_returns_summary():
    """Should return the Wikipedia extract string."""
    mock_response = _make_mock_response(
        "Artificial intelligence (AI) is intelligence demonstrated by machines."
    )
    with patch("app.services.fact_checker.requests.get", return_value=mock_response):
        result = fact_checker.fact_check("Artificial Intelligence")
    assert isinstance(result, str)
    assert len(result) > 10


def test_fact_checker_returns_correct_extract():
    """Should return the exact extract from the API response."""
    expected = "Blockchain is a system of recording information."
    mock_response = _make_mock_response(expected)
    with patch("app.services.fact_checker.requests.get", return_value=mock_response):
        result = fact_checker.fact_check("blockchain")
    assert result == expected


# ── Missing-data path ──────────────────────────────────────────────────────────

def test_fact_checker_missing_extract():
    """Should return fallback message when 'extract' key is absent."""
    mock_response = _make_mock_response("")
    with patch("app.services.fact_checker.requests.get", return_value=mock_response):
        result = fact_checker.fact_check("xyzzy_nonexistent_topic")
    assert isinstance(result, str)
    assert "No summary found" in result


# ── Error-path tests ───────────────────────────────────────────────────────────

def test_fact_checker_handles_connection_error():
    """Should return a user-friendly string on ConnectionError."""
    import requests as req
    with patch("app.services.fact_checker.requests.get",
               side_effect=req.exceptions.ConnectionError):
        result = fact_checker.fact_check("some topic")
    assert isinstance(result, str)
    assert "failed" in result.lower() or "connect" in result.lower()


def test_fact_checker_handles_timeout():
    """Should return a user-friendly string on Timeout."""
    import requests as req
    with patch("app.services.fact_checker.requests.get",
               side_effect=req.exceptions.Timeout):
        result = fact_checker.fact_check("some topic")
    assert isinstance(result, str)
    assert "failed" in result.lower() or "timed out" in result.lower()


def test_fact_checker_handles_generic_exception():
    """Should not raise on unexpected errors."""
    with patch("app.services.fact_checker.requests.get", side_effect=Exception("boom")):
        result = fact_checker.fact_check("some topic")
    assert isinstance(result, str)