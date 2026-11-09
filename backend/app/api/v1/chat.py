"""
Chat endpoints — travel assistant powered by ibm/granite-4-h-small.

Routes:
    POST /api/v1/chat/message         — send a message, receive AI reply
    GET  /api/v1/chat/{session_id}    — retrieve a chat session from Cloudant
"""
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["Chat"])


# TODO Phase 7: implement chat message endpoint
# TODO Phase 7: implement session retrieval endpoint
