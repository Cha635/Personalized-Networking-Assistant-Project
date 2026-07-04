# pyrefly: ignore [missing-import]
from transformers import pipeline, set_seed
from app.config import MODEL_NAMES

# Load the text-generation pipeline once at module level
generator = pipeline("text-generation", model=MODEL_NAMES["text_generator"])


def generate_topics(event_themes: list, user_interests: list) -> list:
    """
    Generate 2-3 conversation starters using GPT-2 Small.

    A structured prompt is built from the extracted event themes and the
    user's declared interests. The raw generated text is split by newline
    and the first three non-empty lines are returned after light cleanup.

    Args:
        event_themes:   List of theme strings from the event analyzer.
        user_interests: List of interest strings provided by the user.

    Returns:
        List of up to 3 conversation-starter strings.
    """
    # Fix seed inside the function so it applies at generation time
    set_seed(42)

    themes_str = ", ".join(event_themes) if event_themes else "general topics"
    interests_str = ", ".join(user_interests) if user_interests else "various subjects"

    prompt = (
        f"I am attending a networking event focused on {themes_str}. "
        f"I am personally interested in {interests_str}. "
        f"Here are three creative and engaging conversation starters I could use:\n"
        f"1."
    )

    outputs = generator(
        prompt,
        max_length=200,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.85,
        pad_token_id=50256,  # GPT-2 EOS token used as pad token
    )

    generated_text = outputs[0]["generated_text"]

    # Extract only the newly generated text (after the prompt)
    generated_portion = generated_text[len(prompt):]

    # Split on newline or numbered list markers
    lines = generated_portion.replace("2.", "\n").replace("3.", "\n").split("\n")
    starters = []
    for line in lines:
        cleaned = line.strip("- ").strip()
        if cleaned and len(cleaned) > 10:
            starters.append(cleaned)
        if len(starters) == 3:
            break

    if starters:
        return starters

    # Fallback: return the first 3 non-empty lines of the full output
    fallback = [ln.strip() for ln in generated_text.split("\n") if ln.strip()]
    return fallback[:3]