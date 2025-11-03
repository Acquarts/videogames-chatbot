from typing import Dict, Any, List, Optional
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

from src.config import settings
from src.utils.logger import get_logger
from src.services.steam_service import SteamService
from src.services.rag_service import RAGService

logger = get_logger()


class ChatbotService:
    """Main chatbot service using Claude with LangChain."""

    def __init__(self):
        """Initialize chatbot with Claude LLM and tools."""
        self.steam_service = SteamService()
        self.rag_service = RAGService()

        # Initialize Claude
        self.llm = ChatAnthropic(
            anthropic_api_key=settings.anthropic_api_key,
            model=settings.claude_model,
            max_tokens=settings.max_tokens,
            temperature=settings.temperature,
        )

        # Create tools for the agent
        self.tools = self._create_tools()

        # System prompt
        self.system_prompt = self._create_system_prompt()

        logger.info(f"Chatbot initialized with model: {settings.claude_model}")

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
5. **Memoria contextual**: Acceso a información histórica y patrones de juegos similares

**Instrucciones:**
- Sé conversacional, amigable y entusiasta sobre videojuegos
- Proporciona análisis profundos cuando se soliciten
- Usa datos concretos de Steam y reseñas reales
- Si no tienes información exacta, búscala primero usando las herramientas disponibles
- Ofrece recomendaciones personalizadas basadas en preferencias del usuario
- Compara juegos cuando sea relevante
- Explica tus análisis con ejemplos de las reseñas

**Formato de respuestas:**
- Usa markdown para mejor legibilidad
- Incluye datos numéricos cuando sean relevantes (puntuaciones, número de reseñas, etc.)
- Cita ejemplos de reseñas cuando analices opiniones
- Estructura respuestas largas con secciones claras

**Limitaciones:**
- Solo puedes acceder a datos públicos de Steam
- No puedes realizar compras ni acceder a cuentas de usuarios
- No inventes datos - si no encuentras información, dilo claramente
"""

    def _create_tools(self) -> List[Tool]:
        """Create LangChain tools for Steam API and RAG."""

        async def search_games_tool(query: str) -> str:
            """Search for games on Steam."""
            results = await self.steam_service.search_games(query, limit=5)
            if not results:
                return f"No se encontraron juegos para: {query}"

            output = f"Encontrados {len(results)} juegos:\n\n"
            for game in results:
                output += f"- {game['name']} (ID: {game['app_id']})\n"
            return output

        async def get_game_info_tool(app_id: str) -> str:
            """Get detailed information about a game."""
            try:
                app_id_int = int(app_id)
                data = await self.steam_service.get_enriched_game_data(app_id_int)

                if not data:
                    return f"No se encontró información para el juego ID: {app_id}"

                # Store in RAG for future queries
                reviews_text = [r["review"] for r in data.get("sample_reviews", [])]
                self.rag_service.add_game_to_knowledge_base(data, reviews_text)

                # Format response
                output = f"**{data['name']}**\n\n"
                output += f"**Descripción**: {data.get('short_description', 'N/A')}\n\n"
                output += f"**Desarrollador**: {', '.join(data.get('developers', ['N/A']))}\n"
                output += f"**Fecha de lanzamiento**: {data.get('release_date', 'N/A')}\n"
                output += f"**Géneros**: {', '.join(data.get('genres', ['N/A']))}\n"
                output += f"**Precio**: {data.get('price', 'N/A')}\n\n"

                if data.get("reviews_summary"):
                    rs = data["reviews_summary"]
                    output += f"**Reseñas**: {rs.get('review_score_desc', 'N/A')}\n"
                    output += f"- Total: {rs.get('total_reviews', 0):,}\n"
                    output += f"- Positivas: {rs.get('total_positive', 0):,}\n"
                    output += f"- Negativas: {rs.get('total_negative', 0):,}\n\n"

                if data.get("metacritic"):
                    output += f"**Metacritic**: {data['metacritic'].get('score', 'N/A')}/100\n\n"

                if data.get("current_players"):
                    output += f"**Jugadores actuales**: {data['current_players']:,}\n"

                return output

            except ValueError:
                return "Error: app_id debe ser un número"
            except Exception as e:
                logger.error(f"Error in get_game_info_tool: {e}")
                return f"Error al obtener información: {str(e)}"

        async def search_knowledge_base_tool(query: str) -> str:
            """Search the knowledge base for similar games or information."""
            results = self.rag_service.search_similar_games(query, n_results=3)

            if not results:
                return "No se encontró información relevante en la base de conocimiento."

            output = "Información relevante encontrada:\n\n"
            for idx, result in enumerate(results, 1):
                output += f"{idx}. {result['document'][:300]}...\n\n"

            return output

        # Return async-compatible tools
        return [
            Tool(
                name="search_games",
                func=lambda q: search_games_tool(q),
                description="Busca juegos en Steam por nombre. Input: nombre del juego a buscar.",
                coroutine=search_games_tool,
            ),
            Tool(
                name="get_game_details",
                func=lambda app_id: get_game_info_tool(app_id),
                description="Obtiene información detallada de un juego específico. Input: app_id (ID numérico del juego en Steam).",
                coroutine=get_game_info_tool,
            ),
            Tool(
                name="search_knowledge",
                func=lambda q: search_knowledge_base_tool(q),
                description="Busca información en la base de conocimiento sobre juegos, reseñas y patrones. Input: consulta de búsqueda.",
                coroutine=search_knowledge_base_tool,
            ),
        ]

    async def chat(
        self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message and generate a response.

        Args:
            message: User message
            conversation_history: Optional list of previous messages

        Returns:
            Dictionary with response and metadata
        """
        try:
            # Build conversation context
            messages = [SystemMessage(content=self.system_prompt)]

            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages
                    if msg["role"] == "user":
                        messages.append(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "assistant":
                        messages.append(AIMessage(content=msg["content"]))

            messages.append(HumanMessage(content=message))

            # Create prompt template
            prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", self.system_prompt),
                    MessagesPlaceholder(variable_name="chat_history", optional=True),
                    ("human", "{input}"),
                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                ]
            )

            # Create agent
            agent = create_tool_calling_agent(self.llm, self.tools, prompt)
            agent_executor = AgentExecutor(
                agent=agent,
                tools=self.tools,
                verbose=True,
                max_iterations=5,
                handle_parsing_errors=True,
            )

            # Execute agent
            result = await agent_executor.ainvoke(
                {"input": message, "chat_history": messages[1:-1]}
            )

            response = result.get("output", "Lo siento, no pude procesar tu solicitud.")

            logger.info(f"Generated response for message: '{message[:50]}...'")

            return {
                "response": response,
                "success": True,
                "metadata": {"model": settings.claude_model, "tools_used": result.get("intermediate_steps", [])},
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
