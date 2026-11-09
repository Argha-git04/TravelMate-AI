"""
IBM Cloudant service — JSON document storage using IBM Cloudant Lite.

SDK: ibmcloudant

Operations:
- Create databases on first use if they do not exist
- Save itinerary documents
- Retrieve itinerary documents
- List all itineraries
- Delete itinerary documents
- Save and retrieve chat session documents

Error handling:
- Returns HTTP 503 if Cloudant credentials are not configured.
- Returns HTTP 404 if a document is not found.
- Never leaks credentials in error messages.
"""

# TODO Phase 5: implement CloudantService class
#   - __init__: validate credentials, create CloudantV1 client
#   - ensure_databases(): create DBs if not present
#   - save_itinerary(doc: dict) -> str  (returns document _id)
#   - get_itinerary(doc_id: str) -> dict
#   - list_itineraries() -> list[dict]
#   - delete_itinerary(doc_id: str) -> None
#   - save_chat_session(doc: dict) -> str
#   - get_chat_session(session_id: str) -> dict
