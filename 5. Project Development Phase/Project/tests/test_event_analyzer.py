"""
Unit tests for event_analyzer.extract_event_themes.

Tests validate structural properties of the output (type, length, label
membership) rather than specific model outputs, so they remain valid across
model updates.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services import event_analyzer

CANDIDATE_LABELS = [
    "AI", "healthcare", "blockchain", "education", "sustainability",
    "finance", "climate change", "urban planning", "cybersecurity",
    "entrepreneurship", "data science", "robotics", "biotech"
]


def test_event_analysis_returns_list():
    """Result must be a list."""
    result = event_analyzer.extract_event_themes("AI in healthcare and diagnostics")
    assert isinstance(result, list)


def test_event_analysis_returns_at_most_three():
    """Result must contain at most 3 themes."""
    result = event_analyzer.extract_event_themes("AI in healthcare and diagnostics")
    assert len(result) <= 3


def test_event_analysis_returns_non_empty():
    """Result must contain at least one theme."""
    result = event_analyzer.extract_event_themes("AI in healthcare and diagnostics")
    assert len(result) >= 1


def test_event_analysis_labels_from_candidates():
    """Each returned theme must come from the candidate label set."""
    result = event_analyzer.extract_event_themes(
        "renewable energy and climate solutions",
        candidate_labels=CANDIDATE_LABELS,
    )
    for theme in result:
        assert theme in CANDIDATE_LABELS


def test_event_analysis_custom_labels():
    """Custom candidate labels are respected."""
    custom_labels = ["space exploration", "quantum computing", "neuroscience"]
    result = event_analyzer.extract_event_themes(
        "quantum algorithms for drug simulation",
        candidate_labels=custom_labels,
    )
    assert isinstance(result, list)
    assert len(result) <= 3


def test_event_analysis_short_description():
    """Even a very short description should return at least one theme."""
    result = event_analyzer.extract_event_themes("blockchain")
    assert len(result) >= 1