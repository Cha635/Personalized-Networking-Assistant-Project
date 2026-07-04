# pyrefly: ignore [missing-import]
from transformers import pipeline
from app.config import MODEL_NAMES

# Load classifier once at module startup for fast inference
classifier = pipeline("zero-shot-classification", model=MODEL_NAMES["event_analysis"])

# Broad set of professional networking themes used as default candidate labels
DEFAULT_LABELS = [
    "AI", "healthcare", "blockchain", "education", "sustainability",
    "finance", "climate change", "urban planning", "cybersecurity",
    "entrepreneurship", "data science", "robotics", "biotech"
]


def extract_event_themes(description: str, candidate_labels=None):
    """
    Extract the top-3 themes from an event description using
    DistilBERT zero-shot classification.

    Args:
        description: Free-text event description.
        candidate_labels: Optional override list of candidate labels.

    Returns:
        List of up to 3 theme strings ranked by confidence.
    """
    if candidate_labels is None:
        candidate_labels = DEFAULT_LABELS

    result = classifier(description, candidate_labels)
    return result["labels"][:3]  # top 3 themes