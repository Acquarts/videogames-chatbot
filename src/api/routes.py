from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from datetime import datetime

from src.api.models import (
    ChatRequest,
    ChatResponse,
    GameSearchRequest,
    GameDetailsRequest,
    GameAnalysisRequest,
    HealthResponse,
    KnowledgeBaseStats,
)
from src.services import SteamService, RAGService, ChatbotService
from src.utils.logger import get_logger
from src import __version__

logger = get_logger()

# Create router
router = APIRouter()

# Initialize services (lazy initialization)
steam_service: SteamService = None
rag_service: RAGService = None
chatbot_service: ChatbotService = None


def get_steam_service():
    """Get or create Steam service instance (lazy initialization)."""
    global steam_service
    if steam_service is None:
        logger.info("Initializing Steam service...")
        steam_service = SteamService()
    return steam_service


def get_rag_service():
    """Get or create RAG service instance (lazy initialization)."""
    global rag_service
    if rag_service is None:
        logger.info("Initializing RAG service...")
        rag_service = RAGService()
    return rag_service


def get_chatbot_service():
    """Get or create Chatbot service instance (lazy initialization)."""
    global chatbot_service
    if chatbot_service is None:
        logger.info("Initializing Chatbot service...")
        chatbot_service = ChatbotService()
    return chatbot_service


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        services_status = {
            "steam_api": steam_service is not None,
            "rag_service": rag_service is not None,
            "chatbot_service": chatbot_service is not None,
        }

        return HealthResponse(
            status="healthy" if all(services_status.values()) else "degraded",
            version=__version__,
            timestamp=datetime.now(),
            services=services_status,
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Service unhealthy"
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint for interacting with the videogame chatbot.

    This endpoint processes user messages and returns AI-generated responses
    with access to Steam API and knowledge base.
    """
    try:
        service = get_chatbot_service()

        if request.use_tools:
            result = await service.chat(
                message=request.message, conversation_history=request.conversation_history
            )
        else:
            response_text = await service.simple_chat(request.message)
            result = {
                "response": response_text,
                "success": True,
                "metadata": {"mode": "simple"},
            }

        return ChatResponse(**result, timestamp=datetime.now())

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/games/search")
async def search_games(request: GameSearchRequest) -> List[Dict[str, Any]]:
    """
    Search for games on Steam.

    Returns a list of games matching the search query.
    """
    try:
        service = get_steam_service()
        results = await service.search_games(request.query, request.limit)
        return results

    except Exception as e:
        logger.error(f"Error searching games: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/games/details")
async def get_game_details(request: GameDetailsRequest) -> Dict[str, Any]:
    """
    Get detailed information about a specific game.

    Returns comprehensive game data including reviews and player count.
    """
    try:
        steam = get_steam_service()
        details = await steam.get_enriched_game_data(request.app_id)

        if not details:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Game with ID {request.app_id} not found",
            )

        # Store in knowledge base
        try:
            rag = get_rag_service()
            reviews_text = [r["review"] for r in details.get("sample_reviews", [])]
            rag.add_game_to_knowledge_base(details, reviews_text)
        except Exception as e:
            logger.warning(f"Could not store in RAG: {e}")

        return details

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting game details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/games/analyze")
async def analyze_game(request: GameAnalysisRequest) -> Dict[str, Any]:
    """
    Analyze game sentiment and characteristics from reviews.

    Uses AI to analyze reviews and provide insights about satisfaction,
    difficulty, originality, artistic level, and more.
    """
    try:
        service = get_chatbot_service()
        analysis = await service.analyze_game_sentiment(request.app_id)

        if "error" in analysis:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=analysis["error"]
            )

        return analysis

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing game: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/knowledge/stats", response_model=KnowledgeBaseStats)
async def get_knowledge_stats():
    """
    Get statistics about the knowledge base.

    Returns information about stored games and reviews.
    """
    try:
        service = get_rag_service()
        stats = service.get_collection_stats()
        return KnowledgeBaseStats(**stats)

    except Exception as e:
        logger.error(f"Error getting knowledge stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.delete("/knowledge/clear")
async def clear_knowledge_base():
    """
    Clear all data from the knowledge base.

    ⚠️ Use with caution! This will delete all stored game information.
    """
    try:
        service = get_rag_service()
        success = service.clear_knowledge_base()

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to clear knowledge base",
            )

        return {"message": "Knowledge base cleared successfully", "success": True}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error clearing knowledge base: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Videogames Chatbot API",
        "version": __version__,
        "description": "AI-powered chatbot for Steam games with RAG capabilities",
        "endpoints": {
            "health": "/health",
            "chat": "/chat",
            "search_games": "/games/search",
            "game_details": "/games/details",
            "analyze_game": "/games/analyze",
            "knowledge_stats": "/knowledge/stats",
        },
        "docs": "/docs",
    }
