import json
from datetime import datetime
from pathlib import Path

# Store feedback.json in the project root's data/ folder
FEEDBACK_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "feedback.json"


def log_feedback(suggestion: str, action: str) -> None:
    """
    Append a user feedback entry to feedback.json.

    Args:
        suggestion: The exact conversation-starter text that was rated.
        action:     Either ``'like'`` or ``'dislike'``.
    """
    entry = {
        "suggestion": suggestion,
        "feedback": action,
        "timestamp": datetime.now().isoformat(),
    }

    FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)

    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(FEEDBACK_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_feedback() -> list:
    """Return all feedback entries, or [] if none exists."""
    if FEEDBACK_FILE.exists():
        with open(FEEDBACK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []