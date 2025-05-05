from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from src.services.DebatorService import DebatorService
from src.schemas.debate_schema import (
    TopicPayload,
    SessionResponse,
    GeneratedArgument,
    FullDebateSession,
)

router = APIRouter()
debator = DebatorService()


@router.post("/debate/generate_session", response_model=SessionResponse)
def generate_session(payload: TopicPayload):
    """
    Create a new debate session for a given topic.
    """
    session_id = debator.generate_session(payload.topic)
    return {"session_id": session_id, "topic": payload.topic}


@router.post("/debate/speak", response_model=GeneratedArgument)
def generate_argument(session_id: str, role: str = Query(..., pattern="^(in-favor|against)$")):
    """
    Generate full-text response from given role in a debate.
    """
    try:
        response = debator.generate_argument(session_id, role)
        return {"session_id": session_id, "role": role, "response": response}
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/debate/stream")
def stream_argument(session_id: str, role: str = Query(..., pattern="^(in-favor|against)$")):
    """
    Stream the next response for a given debate role.
    """
    try:
        stream = debator.stream_argument(session_id, role)
        return StreamingResponse((chunk for chunk in stream), media_type="text/plain")
    except ValueError:
        raise HTTPException(status_code=404, detail="Session not found")


@router.get("/debate/session/{session_id}", response_model=FullDebateSession)
def get_session(session_id: str):
    """
    Retrieve full session JSON for a given session ID.
    """
    session = debator.get_session_data(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, **session}
