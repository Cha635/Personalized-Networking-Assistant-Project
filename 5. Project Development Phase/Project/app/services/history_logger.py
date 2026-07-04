import json
from datetime import datetime
from pathlib import Path

# Store history.json in the project root regardless of working directory
HISTORY_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "history.json"


def log_conversation(data: dict) -> None:
    """
    Append a conversation session to history.json.

    A UTC-formatted timestamp is automatically injected into the record.

    Args:
        data: Dictionary containing description, interests, topics, suggestions.
    """
    data["timestamp"] = datetime.now().isoformat()

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.append(data)

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_history() -> list:
    """Return the full conversation history list, or [] if none exists."""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []