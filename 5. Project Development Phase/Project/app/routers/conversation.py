# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from app.models.schemas import (
    EventInput,
    ConversationRequest,
    FactCheckRequest,
    ConversationResponse,
    FactCheckResponse,
)
from app.services import event_analyzer, topic_generator, fact_checker, history_logger

router = APIRouter()


@router.post("/analyze-event", summary="Extract themes from an event description")
def analyze_event(data: EventInput):
    """
    Run DistilBERT zero-shot classification on the event description
    and return the top-3 extracted themes.
    """
    themes = event_analyzer.extract_event_themes(data.description)
    return {"topics": themes}


@router.post(
    "/fact-check",
    response_model=FactCheckResponse,
    summary="Fact-check a topic via Wikipedia",
)
def fact_check(data: FactCheckRequest):
    """
    Query the Wikipedia REST API and return a short summary
    for the given search term.
    """
    summary = fact_checker.fact_check(data.query)
    return FactCheckResponse(summary=summary)


@router.post(
    "/generate-conversation",
    response_model=ConversationResponse,
    summary="Generate conversation starters for a networking event",
)
def generate_conversation(data: ConversationRequest):
    """
    Full pipeline:
    1. Extract themes from the event description (DistilBERT).
    2. Generate 2-3 conversation starters (GPT-2).
    3. Persist the session to history.json automatically.
    """
    themes = event_analyzer.extract_event_themes(data.description)
    suggestions = topic_generator.generate_topics(themes, data.interests)

    # Persist to history – convert interests to plain list for JSON serialisation
    history_logger.log_conversation({
        "description": data.description,
        "interests": list(data.interests),
        "topics": themes,
        "suggestions": suggestions,
    })

    return ConversationResponse(topics=themes, suggestions=suggestions)