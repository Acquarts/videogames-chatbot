import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from src.config import settings
from src.utils.logger import get_logger

logger = get_logger()


class RAGService:
    """Service for RAG (Retrieval Augmented Generation) using ChromaDB."""

    def __init__(self):
        """Initialize ChromaDB client and collection."""
        try:
            # Initialize ChromaDB with persistent storage
            self.client = chromadb.PersistentClient(
                path=settings.chroma_persist_dir,
                settings=ChromaSettings(
                    anonymized_telemetry=False,
                    allow_reset=True,
                ),
            )

            # Create or get collection for games
            self.games_collection = self.client.get_or_create_collection(
                name="games_knowledge",
                metadata={"description": "Videogame information and reviews"},
            )

            logger.info(
                f"ChromaDB initialized with {self.games_collection.count()} documents"
            )

        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            raise

    def add_game_to_knowledge_base(
        self, game_data: Dict[str, Any], reviews: Optional[List[str]] = None
    ) -> bool:
        """
        Add game information to the knowledge base.

        Args:
            game_data: Dictionary containing game information
            reviews: Optional list of review texts

        Returns:
            True if successful, False otherwise
        """
        try:
            app_id = str(game_data.get("app_id"))
            game_name = game_data.get("name", "Unknown")

            # Create document from game data
            documents = []
            metadatas = []
            ids = []

            # Add main game information
            main_doc = self._create_game_document(game_data)
            documents.append(main_doc)
            metadatas.append(
                {
                    "app_id": app_id,
                    "name": game_name,
                    "type": "game_info",
                    "timestamp": datetime.now().isoformat(),
                }
            )
            ids.append(f"game_{app_id}")

            # Add reviews if provided
            if reviews:
                for idx, review in enumerate(reviews[:20]):  # Limit to 20 reviews
                    if review and len(review.strip()) > 50:  # Only meaningful reviews
                        documents.append(review)
                        metadatas.append(
                            {
                                "app_id": app_id,
                                "name": game_name,
                                "type": "review",
                                "review_index": idx,
                                "timestamp": datetime.now().isoformat(),
                            }
                        )
                        ids.append(f"review_{app_id}_{idx}")

            # Add to collection
            self.games_collection.add(
                documents=documents, metadatas=metadatas, ids=ids
            )

            logger.info(
                f"Added game '{game_name}' with {len(documents)} documents to knowledge base"
            )
            return True

        except Exception as e:
            logger.error(f"Error adding game to knowledge base: {e}")
            return False

    def _create_game_document(self, game_data: Dict[str, Any]) -> str:
        """
        Create a text document from game data for embedding.

        Args:
            game_data: Game information dictionary

        Returns:
            Formatted text document
        """
        doc_parts = []

        # Basic info
        doc_parts.append(f"Game: {game_data.get('name', 'Unknown')}")
        doc_parts.append(f"Type: {game_data.get('type', 'Unknown')}")

        # Description
        if game_data.get("short_description"):
            doc_parts.append(f"Description: {game_data['short_description']}")

        # Developers and Publishers
        if game_data.get("developers"):
            doc_parts.append(f"Developers: {', '.join(game_data['developers'])}")
        if game_data.get("publishers"):
            doc_parts.append(f"Publishers: {', '.join(game_data['publishers'])}")

        # Release date
        if game_data.get("release_date"):
            doc_parts.append(f"Release Date: {game_data['release_date']}")

        # Genres and Categories
        if game_data.get("genres"):
            doc_parts.append(f"Genres: {', '.join(game_data['genres'])}")
        if game_data.get("categories"):
            doc_parts.append(f"Categories: {', '.join(game_data['categories'][:5])}")

        # Reviews summary
        if game_data.get("reviews_summary"):
            reviews_summary = game_data["reviews_summary"]
            total = reviews_summary.get("total_reviews", 0)
            positive = reviews_summary.get("total_positive", 0)
            desc = reviews_summary.get("review_score_desc", "No reviews")

            if total > 0:
                satisfaction = (positive / total * 100) if total > 0 else 0
                doc_parts.append(
                    f"User Reviews: {desc} ({satisfaction:.1f}% positive, {total:,} total reviews)"
                )

        # Metacritic score
        if game_data.get("metacritic") and game_data["metacritic"].get("score"):
            doc_parts.append(f"Metacritic Score: {game_data['metacritic']['score']}/100")

        # Recommendations
        if game_data.get("recommendations"):
            doc_parts.append(f"Recommendations: {game_data['recommendations']:,}")

        # Price
        if game_data.get("price"):
            doc_parts.append(f"Price: {game_data['price']}")

        return "\n".join(doc_parts)

    def search_similar_games(
        self, query: str, n_results: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar games based on semantic similarity.

        Args:
            query: Search query
            n_results: Number of results to return
            filters: Optional metadata filters

        Returns:
            List of matching documents with metadata
        """
        try:
            where_filter = filters if filters else None

            results = self.games_collection.query(
                query_texts=[query], n_results=n_results, where=where_filter
            )

            formatted_results = []
            if results and results["documents"]:
                for idx in range(len(results["documents"][0])):
                    formatted_results.append(
                        {
                            "document": results["documents"][0][idx],
                            "metadata": results["metadatas"][0][idx],
                            "distance": results["distances"][0][idx]
                            if results.get("distances")
                            else None,
                        }
                    )

            logger.info(f"Found {len(formatted_results)} results for query: '{query}'")
            return formatted_results

        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []

    def get_game_context(self, app_id: int) -> Optional[str]:
        """
        Get all stored information about a specific game.

        Args:
            app_id: Steam application ID

        Returns:
            Formatted context string or None
        """
        try:
            results = self.games_collection.get(
                where={"app_id": str(app_id)}, include=["documents", "metadatas"]
            )

            if not results or not results["documents"]:
                return None

            context_parts = []
            for doc, meta in zip(results["documents"], results["metadatas"]):
                if meta.get("type") == "game_info":
                    context_parts.insert(0, doc)  # Game info first
                else:
                    context_parts.append(doc)

            return "\n\n".join(context_parts)

        except Exception as e:
            logger.error(f"Error getting game context for {app_id}: {e}")
            return None

    def delete_game(self, app_id: int) -> bool:
        """
        Delete all information about a game from the knowledge base.

        Args:
            app_id: Steam application ID

        Returns:
            True if successful, False otherwise
        """
        try:
            self.games_collection.delete(where={"app_id": str(app_id)})
            logger.info(f"Deleted game {app_id} from knowledge base")
            return True
        except Exception as e:
            logger.error(f"Error deleting game {app_id}: {e}")
            return False

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge base.

        Returns:
            Dictionary with collection statistics
        """
        try:
            total_docs = self.games_collection.count()

            # Get sample of metadata to count types
            sample = self.games_collection.get(limit=1000, include=["metadatas"])

            game_count = sum(
                1 for meta in sample["metadatas"] if meta.get("type") == "game_info"
            )
            review_count = sum(
                1 for meta in sample["metadatas"] if meta.get("type") == "review"
            )

            return {
                "total_documents": total_docs,
                "estimated_games": game_count,
                "estimated_reviews": review_count,
                "collection_name": self.games_collection.name,
            }

        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"total_documents": 0, "estimated_games": 0, "estimated_reviews": 0}

    def clear_knowledge_base(self) -> bool:
        """
        Clear all data from the knowledge base. Use with caution!

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_collection(name="games_knowledge")
            self.games_collection = self.client.create_collection(
                name="games_knowledge",
                metadata={"description": "Videogame information and reviews"},
            )
            logger.warning("Knowledge base cleared!")
            return True
        except Exception as e:
            logger.error(f"Error clearing knowledge base: {e}")
            return False
