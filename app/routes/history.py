"""
history_route.py

This module defines an API endpoint to retrieve the history of text summarizations
stored in the database.

It exposes a GET endpoint that returns the most recent summarization records,
including the input text, generated summary, model and provider used, and timestamp.

Features:
- Supports an optional query parameter 'limit' to specify the number of records returned (default 10).
- Results are sorted by creation date in descending order (most recent first).
- Converts MongoDB ObjectId to string for JSON serialization.

Dependencies:
- FastAPI for routing and dependency injection.
- Database dependency injected via Depends(get_db).

Usage:
- Send a GET request to the root path ('') optionally with ?limit=number.
- Receives a JSON response containing an array of summary history records under the "history" key.

Example response:
{
    "history": [
        {
            "_id": "605c3b2f8c4a5b6d3a5e9c15",
            "input_text": "Some input text...",
            "summary_text": "Generated summary...",
            "model": "gpt-3.5-turbo",
            "provider": "openai",
            "created_at": "2025-05-17T06:00:00Z"
        },
        ...
    ]
}
"""


from fastapi import APIRouter, Depends
from app.dependencies import get_db

router = APIRouter()

@router.get("")
async def get_history(limit: int = 10, db=Depends(get_db)):

    """
    Retrieve the most recent summarization history entries.

    Args:
        limit (int): Maximum number of history records to return (default is 10).
        db: Database dependency injected by FastAPI.

    Returns:
        dict: A dictionary with a "history" key containing a list of summary documents.
              Each document includes input text, summary, model, provider, and creation timestamp.
    """

    cursor = db.summaries.find().sort("created_at", -1).limit(limit)
    results = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        results.append(doc)
    return {"history": results}
