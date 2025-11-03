"""
Simplified chatbot service without complex LangChain agents.
Uses direct Claude API with tool calling.
"""

from typing import Dict, Any, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool

from src.config import settings
from src.utils.logger import get_logger
from src.services.steam_service import SteamService
from src.services.rag_service import RAGService

logger = get_logger()


class ChatbotService:
    """Main chatbot service using Claude with direct tool calling."""

    def __init__(self):
        """Initialize chatbot with Claude LLM."""
        self.steam_service = SteamService()
        self.rag_service = RAGService()

        # Define tools
        self.tools = self._create_tools()

        # Initialize Claude with tools
        self.llm = ChatAnthropic(
            anthropic_api_key=settings.anthropic_api_key,
            model=settings.claude_model,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
        ).bind_tools(self.tools)

        # System prompt
        self.system_prompt = self._create_system_prompt()

        logger.info(f"Chatbot initialized with model: {settings.claude_model}")

    def _create_tools(self) -> List:
        """Create tool definitions for Claude."""
        steam_service = self.steam_service

        @tool
        async def search_steam_games(query: str, limit: int = 5) -> str:
            """
            Search for games on Steam by name or keyword.

            Args:
                query: Game name or search keyword
                limit: Maximum number of results (default 5)

            Returns:
                JSON string with list of games including app_id, name, and brief info
            """
            try:
                results = await steam_service.search_games(query, limit=limit)
                if not results:
                    return f"No se encontraron juegos para '{query}'"

                import json
                return json.dumps(results, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error in search_steam_games: {e}")
                return f"Error al buscar juegos: {str(e)}"

        @tool
        async def get_game_details(app_id: int) -> str:
            """
            Get detailed information about a specific Steam game.

            Args:
                app_id: Steam application ID

            Returns:
                JSON string with comprehensive game details
            """
            try:
                details = await steam_service.get_game_details(app_id)
                if not details:
                    return f"No se pudo obtener información del juego {app_id}"

                import json
                return json.dumps(details, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error in get_game_details: {e}")
                return f"Error al obtener detalles: {str(e)}"

        @tool
        async def get_game_reviews(app_id: int, num_reviews: int = 20) -> str:
            """
            Get user reviews for a Steam game.

            Args:
                app_id: Steam application ID
                num_reviews: Number of reviews to fetch (default 20)

            Returns:
                JSON string with review data and statistics
            """
            try:
                reviews = await steam_service.get_game_reviews(app_id, num_reviews=num_reviews)
                if not reviews:
                    return f"No se pudieron obtener reseñas del juego {app_id}"

                import json
                return json.dumps(reviews, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error in get_game_reviews: {e}")
                return f"Error al obtener reseñas: {str(e)}"

        return [search_steam_games, get_game_details, get_game_reviews]

    def _create_system_prompt(self) -> str:
        """Create comprehensive system prompt for the chatbot."""
        return """Eres un asistente experto en videojuegos conectado a la API de Steam. Tu propósito es ayudar a usuarios a descubrir, analizar y obtener información detallada sobre videojuegos.

**Capacidades:**
1. **Búsqueda de juegos**: Puedes buscar juegos en Steam por nombre
2. **Información detallada**: Acceso a datos completos incluyendo:
   - Descripciones y desarrolladores
   - Fechas de lanzamiento
   - Precios y plataformas
   - Géneros y categorías
   - Puntuaciones Metacritic
3. **Análisis de reseñas**: Evaluación de opiniones de usuarios para determinar:
   - Nivel de satisfacción
   - Aspectos positivos y negativos
   - Dificultad percibida
   - Originalidad
   - Calidad artística
4. **Datos de jugadores**: Información sobre jugadores activos y popularidad

**Instrucciones:**
- Sé conversacional, amigable y entusiasta sobre videojuegos
- Usa las herramientas disponibles para obtener datos reales de Steam
- Proporciona análisis profundos basados en datos concretos
- Ofrece recomendaciones personalizadas basadas en preferencias del usuario
- NO muestres las llamadas a herramientas en tus respuestas, solo los resultados
- Presenta la información de forma clara y estructurada

**Formato de respuestas:**
- Usa markdown para mejor legibilidad
- Incluye datos numéricos cuando sean relevantes (puntuaciones, número de reseñas, etc.)
- Estructura respuestas largas con secciones claras

**Limitaciones:**
- Solo puedes acceder a datos públicos de Steam
- No puedes realizar compras ni acceder a cuentas de usuarios
- No inventes datos - usa las herramientas para obtener información real
"""

    async def chat(
        self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and generate a response with tool calling support.

        Args:
            message: User message
            conversation_history: Optional list of previous messages

        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build conversation context
            messages = [SystemMessage(content=self.system_prompt)]

            if conversation_history and isinstance(conversation_history, list):
                for msg in conversation_history[-10:]:  # Keep last 10 messages
                    if isinstance(msg, dict):
                        role = msg.get("role", "")
                        content = msg.get("content", "")
                        if role == "user" and content:
                            messages.append(HumanMessage(content=content))
                        elif role == "assistant" and content:
                            messages.append(AIMessage(content=content))

            # Add user message
            messages.append(HumanMessage(content=message))

            # Tool calling loop
            max_iterations = 5
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # Get response from Claude
                response = await self.llm.ainvoke(messages)
                messages.append(response)

                # Check if tool calls are present
                if not response.tool_calls:
                    # No more tool calls, return final response
                    logger.info(f"Generated final response for message: '{message[:50]}...'")
                    return {
                        "response": response.content,
                        "success": True,
                        "metadata": {
                            "model": settings.claude_model,
                            "tool_calls": iteration - 1,
                        },
                    }

                # Execute tool calls
                logger.info(f"Executing {len(response.tool_calls)} tool calls")
                for tool_call in response.tool_calls:
                    tool_name = tool_call["name"]
                    tool_args = tool_call["args"]
                    tool_id = tool_call["id"]

                    logger.info(f"Calling tool: {tool_name} with args: {tool_args}")

                    # Find and execute the tool
                    tool_result = None
                    for tool in self.tools:
                        if tool.name == tool_name:
                            tool_result = await tool.ainvoke(tool_args)
                            break

                    if tool_result is None:
                        tool_result = f"Error: Tool {tool_name} not found"

                    # Add tool result to messages
                    messages.append(
                        ToolMessage(
                            content=str(tool_result),
                            tool_call_id=tool_id,
                        )
                    )

            # Max iterations reached
            logger.warning("Max tool iterations reached")
            return {
                "response": "Lo siento, la consulta es demasiado compleja. Por favor, intenta dividirla en preguntas más específicas.",
                "success": False,
                "metadata": {"error": "max_iterations_reached"},
            }

        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": f"Lo siento, ocurrió un error: {str(e)}",
                "success": False,
                "metadata": {"error": str(e)},
            }

    async def simple_chat(self, message: str) -> str:
        """
        Simple chat without tools for basic queries.

        Args:
            message: User message

        Returns:
            Response string
        """
        try:
            messages = [
                SystemMessage(content=self.system_prompt),
                HumanMessage(content=message),
            ]

            response = await self.llm.ainvoke(messages)
            return response.content

        except Exception as e:
            logger.error(f"Error in simple_chat: {e}")
            return f"Lo siento, ocurrió un error: {str(e)}"

    async def analyze_game_sentiment(self, app_id: int) -> Dict[str, Any]:
        """
        Analyze sentiment and characteristics from game reviews.

        Args:
            app_id: Steam application ID

        Returns:
            Analysis dictionary
        """
        try:
            # Get reviews
            reviews_data = await self.steam_service.get_game_reviews(app_id, num_reviews=50)
            game_details = await self.steam_service.get_game_details(app_id)

            if not reviews_data or not game_details:
                return {"error": "No se pudo obtener información del juego"}

            # Prepare review samples
            sample_reviews = "\n\n".join(
                [r["review"][:500] for r in reviews_data.get("reviews", [])[:10]]
            )

            # Create analysis prompt
            analysis_prompt = f"""Analiza las siguientes reseñas del juego "{game_details['name']}" y proporciona:

1. **Nivel de satisfacción general** (1-10)
2. **Dificultad percibida** (Fácil/Media/Difícil/Muy Difícil)
3. **Originalidad** (1-10)
4. **Nivel artístico** (1-10)
5. **Aspectos más valorados** (3-5 puntos)
6. **Aspectos más criticados** (3-5 puntos)
7. **Horas de juego promedio** según las reseñas
8. **Recomendación** para qué tipo de jugador

Reseñas (muestra de {len(reviews_data.get('reviews', []))} total):
{sample_reviews}

Estadísticas generales:
- Total reseñas: {reviews_data.get('total_reviews', 0):,}
- Positivas: {reviews_data.get('total_positive', 0):,}
- Negativas: {reviews_data.get('total_negative', 0):,}
- Descripción: {reviews_data.get('review_score_desc', 'N/A')}
"""

            response = await self.simple_chat(analysis_prompt)

            return {
                "game_name": game_details["name"],
                "app_id": app_id,
                "analysis": response,
                "review_stats": {
                    "total": reviews_data.get("total_reviews", 0),
                    "positive": reviews_data.get("total_positive", 0),
                    "negative": reviews_data.get("total_negative", 0),
                    "score_desc": reviews_data.get("review_score_desc", "N/A"),
                },
            }

        except Exception as e:
            logger.error(f"Error analyzing game sentiment: {e}")
            return {"error": str(e)}

    async def close(self):
        """Close all service connections."""
        await self.steam_service.close()
        logger.info("Chatbot services closed")
