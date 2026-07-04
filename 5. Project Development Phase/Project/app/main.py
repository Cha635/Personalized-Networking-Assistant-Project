# pyrefly: ignore [missing-import]
from fastapi import FastAPI
from app.routers import conversation

app = FastAPI(
    title="Personalized Networking Assistant",
    description=(
        "AI-powered API that extracts themes from networking event descriptions "
        "using DistilBERT and generates conversation starters using GPT-2. "
        "Includes Wikipedia-based fact-checking."
    ),
    version="1.0.0",
)

app.include_router(conversation.router, prefix="", tags=["Conversation"])


@app.get("/", tags=["Health"])
def root():
    """Health-check endpoint – confirms the API is running."""
    return {"message": "Welcome to the Networking Assistant API!", "status": "ok"}