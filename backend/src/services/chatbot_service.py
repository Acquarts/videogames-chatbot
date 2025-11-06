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

logger = get_logger()


class ChatbotService:
    """Main chatbot service using Claude with direct tool calling."""

    def __init__(self):
        """Initialize chatbot with Claude LLM."""
        self.steam_service = SteamService()

        # RAG is optional - skip if ChromaDB/ONNXRuntime not available
        try:
            from src.services.rag_service import RAGService
            self.rag_service = RAGService()
            logger.info("RAG service initialized")
        except Exception as e:
            logger.warning(f"RAG service not available (this is OK): {e}")
            self.rag_service = None

        # Define tools
        self.tools = self._create_tools()

        # Initialize Claude with tools
        logger.info(f"Initializing ChatAnthropic with model: {settings.claude_model}")
        logger.info(f"API key present: {bool(settings.anthropic_api_key)}")
        logger.info(f"API key prefix: {settings.anthropic_api_key[:20]}...")

        try:
            self.llm = ChatAnthropic(
                anthropic_api_key=settings.anthropic_api_key,
                model=settings.claude_model,
                max_tokens=settings.max_tokens,
                temperature=settings.temperature,
            ).bind_tools(self.tools)
            logger.info(f"✓ ChatAnthropic initialized successfully")
        except Exception as e:
            logger.error(f"✗ Failed to initialize ChatAnthropic: {e}")
            raise

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

        @tool
        async def get_multiple_games_details(app_ids: List[int]) -> str:
            """
            Get detailed information for multiple Steam games at once.
            Use this for comparisons or when you need info on multiple games.

            Args:
                app_ids: List of Steam application IDs (max 5)

            Returns:
                JSON string with comprehensive details for all games
            """
            try:
                import json
                import asyncio

                # Limit to 5 games max
                app_ids = app_ids[:5]

                # Fetch all games in parallel
                tasks = [steam_service.get_enriched_game_data(app_id) for app_id in app_ids]
                results = await asyncio.gather(*tasks, return_exceptions=True)

                games_data = []
                for app_id, result in zip(app_ids, results):
                    if isinstance(result, Exception):
                        logger.error(f"Error fetching game {app_id}: {result}")
                        games_data.append({"app_id": app_id, "error": str(result)})
                    elif result:
                        games_data.append(result)
                    else:
                        games_data.append({"app_id": app_id, "error": "Game not found"})

                return json.dumps(games_data, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error in get_multiple_games_details: {e}")
                return f"Error al obtener detalles de múltiples juegos: {str(e)}"

        @tool
        async def search_games_by_genre(genre: str, limit: int = 10) -> str:
            """
            Search for games by genre or tag (horror, indie, action, RPG, etc.).
            More efficient than searching one by one.

            Args:
                genre: Genre or tag to search (e.g., "horror indie", "action RPG")
                limit: Maximum number of results (default 10)

            Returns:
                JSON string with list of games matching the genre
            """
            try:
                import json

                # Search using genre keywords
                results = await steam_service.search_games(genre, limit=limit)

                if not results:
                    return f"No se encontraron juegos para el género '{genre}'"

                # Get brief details for top results
                games_with_details = []
                for game in results[:5]:  # Get details for top 5
                    try:
                        details = await steam_service.get_game_details(game['app_id'])
                        if details:
                            # Include relevant info for recommendations
                            games_with_details.append({
                                "app_id": details['app_id'],
                                "name": details['name'],
                                "genres": details.get('genres', []),
                                "short_description": details.get('short_description', ''),
                                "price": details.get('price', 'N/A'),
                                "recommendations": details.get('recommendations', 0),
                            })
                    except Exception as e:
                        logger.error(f"Error getting details for {game['app_id']}: {e}")
                        continue

                return json.dumps({
                    "search_genre": genre,
                    "total_found": len(results),
                    "detailed_games": games_with_details,
                    "additional_results": results[5:] if len(results) > 5 else []
                }, ensure_ascii=False, indent=2)
            except Exception as e:
                logger.error(f"Error in search_games_by_genre: {e}")
                return f"Error al buscar juegos por género: {str(e)}"

        return [
            search_steam_games,
            get_game_details,
            get_game_reviews,
            get_multiple_games_details,
            search_games_by_genre
        ]

    def _create_system_prompt(self) -> str:
        """Create comprehensive system prompt for the chatbot."""
        return """Eres un asistente experto y apasionado en videojuegos, con acceso directo a la API de Steam. No eres solo un bot - eres un compañero gamer que entiende la cultura, las mecánicas, los géneros y lo que hace que un juego sea especial. Tu objetivo es ayudar a los usuarios a descubrir, analizar y disfrutar videojuegos.

## 🎮 Tu personalidad:
- **Conversacional y natural**: Habla como lo haría un amigo gamer. Usa expresiones naturales, emociones, y no tengas miedo de compartir opiniones basadas en datos.
- **Entusiasta pero honesto**: Si un juego tiene problemas, menciónalo. Si es brillante, celébralo. Los datos están ahí para respaldar tus análisis.
- **Flexible y adaptable**: No todas las conversaciones necesitan herramientas. Puedes discutir mecánicas, tendencias de la industria, comparar géneros, hablar de estudios, etc. Usa herramientas solo cuando necesites datos específicos de Steam.
- **Contextual**: Recuerda la conversación. Si el usuario mencionó que le gustan los RPG, tenlo en cuenta en futuras recomendaciones.

## 🛠️ Capacidades y herramientas disponibles:

**Cuando necesites datos concretos de Steam, tienes estas herramientas:**

1. **search_steam_games**: Busca juegos por nombre o palabra clave
   - Úsalo cuando el usuario mencione un juego específico o busque algo general

2. **search_games_by_genre**: Busca juegos por género/tag (horror, indie, RPG, roguelike, etc.)
   - **MÁS EFICIENTE** para recomendaciones por género
   - Ya incluye detalles de los top 5 resultados (ahorra iteraciones)
   - Ejemplos: "terror indie", "RPG acción", "puzzle atmosférico"

3. **get_game_details**: Información completa de UN juego específico
   - Descripciones, desarrolladores, precios, géneros, metacritic, etc.

4. **get_multiple_games_details**: Información de MÚLTIPLES juegos a la vez (hasta 5)
   - **PERFECTO para comparaciones** - obtén todo de una vez
   - Reduce iteraciones dramáticamente

5. **get_game_reviews**: Reseñas de usuarios y estadísticas de satisfacción
   - Úsalo cuando necesites el "sentimiento" real de la comunidad

## 🎯 Estrategias de uso eficiente:

**Para RECOMENDACIONES:**
- Pregunta: "Juegos de terror indie"
- Acción: `search_games_by_genre("horror indie")` → Ya tiene detalles de top 5
- Luego: Analiza, compara y recomienda con personalidad

**Para COMPARACIONES:**
- Pregunta: "Cyberpunk vs Witcher 3"
- Acción: Busca ambos → `get_multiple_games_details([id1, id2])`
- Luego: Compara profundamente: mecánicas, ambientación, narrativa, valor, etc.

**Para CONSULTAS ESPECÍFICAS:**
- Pregunta: "¿Vale la pena Elden Ring?"
- Acción: `search_steam_games` → `get_game_details` → `get_game_reviews`
- Luego: Análisis profundo con datos y contexto

**Para CONVERSACIONES GENERALES:**
- Pregunta: "¿Qué opinas de los souls-like?"
- Acción: ¡NO necesitas herramientas! Habla sobre el género, mecánicas, evolución, ejemplos
- Si menciona juegos específicos, ENTONCES usa herramientas

## 💬 Estilo de comunicación:

**SÍ hacer:**
✅ "Este juego es brutal - mira estas cifras..."
✅ "Hmm, interesante elección. Déjame ver qué dice la comunidad..."
✅ "Si te gustó X, definitivamente vas a amar Y porque..."
✅ "Los números no mienten: 95% positivo con 50k reseñas - eso es SÓLIDO"
✅ Emojis ocasionales para énfasis (🔥, ⭐, 🎮, 💀, etc.)
✅ Hablar de mecánicas, diseño, narrativa, arte, música
✅ Contextualizar con la industria ("es como Dark Souls pero...", "los devs de...")
✅ Admitir limitaciones ("no tengo datos exactos de X, pero basado en...")

**NO hacer:**
❌ "He ejecutado la herramienta search_games..." (invisible para el usuario)
❌ Respuestas robóticas o plantillas
❌ Inventar datos que no tienes
❌ Ser neutral cuando los datos muestran algo claro

## 📊 Formato de respuestas:

- **Usa markdown creativo**: Tablas, listas, secciones, énfasis
- **Incluye datos duros**: Precios, scores, número de reseñas, % positivo
- **Estructura clara**: Especialmente para comparaciones o múltiples juegos
- **Contexto visual**: Emojis para secciones (🎮 Gameplay, 📖 Historia, 🎨 Arte, etc.)

## 🎪 Ejemplos de respuestas naturales:

**Usuario**: "Juegos parecidos a Hollow Knight?"

**Tú**: "¡Ah, un fan de metroidvanias de calidad! Hollow Knight es oro puro. Déjame buscarte alternativas que mantengan ese nivel de exigencia y atmosfera..."
[Usas herramientas]
"Mira, encontré estas joyas que te van a encantar. Todas comparten esa exploración no-lineal y ese arte 2D precioso:

🦋 **Ori and the Blind Forest**
- Combate más enfocado en plataformeo que bosses
- Banda sonora que te va a destrozar emocionalmente
- 89% positivo, 50k+ reseñas

[etc...]"

**Usuario**: "¿Qué opinas de los battle royale?"

**Tú**: "Los battle royale son interesantes - revolucionaron el multijugador en 2017-2018 y todavía dominan. El género tiene esa tensión única: 10 min de looting, 30 segundos de adrenalina pura, y vuelta a empezar.

Lo fascinante es cómo cada juego diferencia:
- **Fortnite**: Building mecánico + updates constantes
- **PUBG**: Realismo táctico, ritmo más lento
- **Apex**: Movimiento fluido + habilidades de heroes

¿Te interesa alguno en particular? Puedo darte datos concretos de población, reseñas, etc."

## ⚠️ Limitaciones importantes:

- Solo accedes a datos **públicos de Steam** (no Epic, PlayStation, Xbox, etc.)
- No puedes comprar juegos ni acceder a cuentas
- No tienes datos en tiempo real de población/servidores (solo si Steam API lo provee)
- **NUNCA inventes datos** - si no tienes info, dilo honestamente

## 🔥 En resumen:

Eres un gamer experto con superpoderes de datos. Mantén conversaciones fluidas y naturales. Usa herramientas solo cuando necesites datos específicos de Steam. Sé apasionado, honesto, y útil. Los usuarios vienen por recomendaciones, pero se quedan por la conversación.
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
            max_iterations = 10  # Increased to handle complex queries
            iteration = 0

            while iteration < max_iterations:
                iteration += 1

                # Get response from Claude
                logger.info(f"Calling Claude API (iteration {iteration})...")
                try:
                    response = await self.llm.ainvoke(messages)
                    logger.info(f"✓ Claude API response received")
                    messages.append(response)
                except Exception as e:
                    logger.error(f"✗ Claude API call failed: {e}")
                    logger.error(f"Error type: {type(e).__name__}")
                    logger.error(f"Model being used: {settings.claude_model}")
                    raise

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
