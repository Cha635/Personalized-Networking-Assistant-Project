"""
Unit tests for topic_generator.generate_topics.

Tests validate structural properties (type, length, string content) without
asserting specific model outputs, ensuring tests remain stable across model
updates.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services import topic_generator


def test_topic_generation_returns_list():
    """Result must be a list."""
    result = topic_generator.generate_topics(["AI", "healthcare"], ["ethics", "automation"])
    assert isinstance(result, list)


def test_topic_generation_returns_non_empty():
    """Result must contain at least one suggestion."""
    result = topic_generator.generate_topics(["AI", "healthcare"], ["ethics", "automation"])
    assert len(result) >= 1


def test_topic_generation_returns_strings():
    """Every suggestion must be a string."""
    result = topic_generator.generate_topics(["blockchain"], ["finance"])
    for suggestion in result:
        assert isinstance(suggestion, str)


def test_topic_generation_non_empty_strings():
    """Every suggestion string must be non-blank."""
    result = topic_generator.generate_topics(["sustainability"], ["green energy"])
    for suggestion in result:
        assert suggestion.strip() != ""


def test_topic_generation_at_most_three():
    """Result must contain at most 3 suggestions."""
    result = topic_generator.generate_topics(
        ["AI", "education", "robotics"], ["automation", "ethics"]
    )
    assert len(result) <= 3


def test_topic_generation_empty_interests():
    """Generator should handle empty interests gracefully."""
    result = topic_generator.generate_topics(["cybersecurity"], [])
    assert isinstance(result, list)
    assert len(result) >= 1