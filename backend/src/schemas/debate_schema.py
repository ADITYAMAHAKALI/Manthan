from pydantic import BaseModel, Field
from typing import Literal, List

class TopicPayload(BaseModel):
    topic: str = Field(..., min_length=3, max_length=200, example="Regulation of AI")

class RoleLiteral(BaseModel):
    role: Literal["in-favor", "against"]

class SessionResponse(BaseModel):
    session_id: str
    topic: str

class DebateMessage(BaseModel):
    role: Literal["in-favor", "against"]
    message: str

class FullDebateSession(BaseModel):
    session_id: str
    topic: str
    history: List[DebateMessage]

class GeneratedArgument(BaseModel):
    session_id: str
    role: Literal["in-favor", "against"]
    response: str
