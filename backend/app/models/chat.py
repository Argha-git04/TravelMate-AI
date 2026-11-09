"""
Pydantic models for chat session requests and responses.
"""
from pydantic import BaseModel
from typing import Optional

# TODO Phase 7: expand with full chat models
#   ChatMessage, ChatSession, ChatRequest, ChatResponse


class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = None    # None = start a new session
    message: str
    history: list[dict] = []            # Previous messages for context
