from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str = Field(..., min_length=1, description="User message")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None, description="Previous conversation messages"
    )
    use_tools: bool = Field(default=True, description="Whether to use tools/agents")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    response: str = Field(..., description="Chatbot response")
    success: bool = Field(..., description="Whether the request was successful")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata"
    )
    timestamp: datetime = Field(default_factory=lambda: datetime.now())


class GameSearchRequest(BaseModel):
    """Request model for game search."""

    query: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(default=10, ge=1, le=50, description="Maximum results")


class GameDetailsRequest(BaseModel):
    """Request model for game details."""

    app_id: int = Field(..., gt=0, description="Steam application ID")


class GameAnalysisRequest(BaseModel):
    """Request model for game sentiment analysis."""

    app_id: int = Field(..., gt=0, description="Steam application ID")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    timestamp: datetime
    services: Dict[str, bool]


class KnowledgeBaseStats(BaseModel):
    """Knowledge base statistics."""

    total_documents: int
    estimated_games: int
    estimated_reviews: int
    collection_name: str
