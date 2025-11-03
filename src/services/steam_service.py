import httpx
from typing import Dict, List, Optional, Any
from src.config import settings
from src.utils.logger import get_logger
from src.utils.cache import cached

logger = get_logger()


class SteamService:
    """Service for interacting with Steam API."""

    def __init__(self):
        self.api_key = settings.steam_api_key
        self.base_url = settings.steam_api_base_url
        self.store_url = settings.steam_store_api_url
        self.client = httpx.AsyncClient(timeout=30.0)

        # Log API key status
        if not self.api_key:
            logger.warning(
                "⚠️  Steam API key not configured. "
                "Most features will work, but 'current player count' will be unavailable."
            )
        else:
            logger.info("✅ Steam API key configured")

    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()

    @cached(prefix="steam_game_details", ttl=86400)  # Cache for 24 hours
    async def get_game_details(self, app_id: int) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a game from Steam Store API.

        Args:
            app_id: Steam application ID

        Returns:
            Game details dictionary or None if not found
        """
        try:
            url = f"{self.store_url}/appdetails"
            params = {"appids": app_id, "l": "english"}

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if str(app_id) in data and data[str(app_id)]["success"]:
                game_data = data[str(app_id)]["data"]

                return {
                    "app_id": app_id,
                    "name": game_data.get("name"),
                    "type": game_data.get("type"),
                    "description": game_data.get("detailed_description"),
                    "short_description": game_data.get("short_description"),
                    "developers": game_data.get("developers", []),
                    "publishers": game_data.get("publishers", []),
                    "price": game_data.get("price_overview", {}).get("final_formatted", "Free"),
                    "release_date": game_data.get("release_date", {}).get("date"),
                    "platforms": game_data.get("platforms", {}),
                    "metacritic": game_data.get("metacritic", {}),
                    "categories": [cat.get("description") for cat in game_data.get("categories", [])],
                    "genres": [genre.get("description") for genre in game_data.get("genres", [])],
                    "screenshots": [ss.get("path_full") for ss in game_data.get("screenshots", [])[:3]],
                    "recommendations": game_data.get("recommendations", {}).get("total", 0),
                }

            logger.warning(f"Game {app_id} not found in Steam Store")
            return None

        except httpx.HTTPError as e:
            logger.error(f"HTTP error getting game details for {app_id}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error getting game details for {app_id}: {e}")
            return None

    @cached(prefix="steam_reviews", ttl=3600)  # Cache for 1 hour
    async def get_game_reviews(self, app_id: int, num_reviews: int = 100) -> Dict[str, Any]:
        """
        Get user reviews for a game.

        Args:
            app_id: Steam application ID
            num_reviews: Number of reviews to fetch

        Returns:
            Reviews data with sentiment analysis
        """
        try:
            url = f"{self.store_url}/appreviews/{app_id}"
            params = {
                "json": 1,
                "language": "english",
                "num_per_page": min(num_reviews, 100),
                "filter": "recent",
            }

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data.get("success") == 1:
                reviews = data.get("reviews", [])
                query_summary = data.get("query_summary", {})

                return {
                    "app_id": app_id,
                    "total_positive": query_summary.get("total_positive", 0),
                    "total_negative": query_summary.get("total_negative", 0),
                    "total_reviews": query_summary.get("total_reviews", 0),
                    "review_score": query_summary.get("review_score", 0),
                    "review_score_desc": query_summary.get("review_score_desc", "No reviews"),
                    "reviews": [
                        {
                            "recommended": review.get("voted_up"),
                            "votes_up": review.get("votes_up"),
                            "votes_funny": review.get("votes_funny"),
                            "playtime_forever": review.get("author", {}).get("playtime_forever", 0),
                            "review": review.get("review"),
                            "timestamp_created": review.get("timestamp_created"),
                        }
                        for review in reviews[:20]  # Limit to 20 reviews
                    ],
                }

            logger.warning(f"No reviews found for game {app_id}")
            return {"app_id": app_id, "total_reviews": 0, "reviews": []}

        except Exception as e:
            logger.error(f"Error getting reviews for {app_id}: {e}")
            return {"app_id": app_id, "total_reviews": 0, "reviews": []}

    @cached(prefix="steam_search", ttl=3600)
    async def search_games(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search for games by name.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching games
        """
        try:
            # Steam doesn't have a direct search API, so we use the store search
            url = f"{self.store_url}/storesearch"
            params = {"term": query, "l": "english", "cc": "US"}

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])

            results = []
            for item in items[:limit]:
                results.append(
                    {
                        "app_id": item.get("id"),
                        "name": item.get("name"),
                        "type": item.get("type"),
                        "tiny_image": item.get("tiny_image"),
                    }
                )

            logger.info(f"Found {len(results)} games for query: {query}")
            return results

        except Exception as e:
            logger.error(f"Error searching games with query '{query}': {e}")
            return []

    async def get_player_count(self, app_id: int) -> Optional[int]:
        """
        Get current player count for a game.

        Note: This endpoint may require API key for some games.

        Args:
            app_id: Steam application ID

        Returns:
            Current player count or None
        """
        # This endpoint works for most games without API key, but not all
        try:
            url = f"{self.base_url}/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
            params = {"appid": app_id}

            # Add API key if available
            if self.api_key:
                params["key"] = self.api_key

            response = await self.client.get(url, params=params)
            response.raise_for_status()

            data = response.json()

            if data.get("response", {}).get("result") == 1:
                return data["response"]["player_count"]

            return None

        except Exception as e:
            if not self.api_key:
                logger.debug(f"Player count unavailable for {app_id} (no API key)")
            else:
                logger.error(f"Error getting player count for {app_id}: {e}")
            return None

    async def get_enriched_game_data(self, app_id: int) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive game data including details, reviews, and player count.

        Args:
            app_id: Steam application ID

        Returns:
            Enriched game data dictionary
        """
        game_details = await self.get_game_details(app_id)

        if not game_details:
            return None

        reviews = await self.get_game_reviews(app_id)
        player_count = await self.get_player_count(app_id)

        # Combine all data
        enriched_data = {
            **game_details,
            "reviews_summary": {
                "total_positive": reviews.get("total_positive", 0),
                "total_negative": reviews.get("total_negative", 0),
                "total_reviews": reviews.get("total_reviews", 0),
                "review_score_desc": reviews.get("review_score_desc", "No reviews"),
            },
            "current_players": player_count,
            "sample_reviews": reviews.get("reviews", [])[:5],  # Top 5 reviews
        }

        return enriched_data
