"""
Simple usage example for Videogames Chatbot
"""

import asyncio
import httpx
import json


async def main():
    """Run simple examples of API usage."""

    base_url = "http://localhost:8000/api/v1"

    async with httpx.AsyncClient(timeout=30.0) as client:
        print("🎮 Videogames Chatbot - Usage Examples\n")

        # 1. Health check
        print("=" * 50)
        print("1. Health Check")
        print("=" * 50)
        response = await client.get(f"{base_url}/health")
        print(json.dumps(response.json(), indent=2))
        print()

        # 2. Search for a game
        print("=" * 50)
        print("2. Searching for 'Baldur's Gate 3'")
        print("=" * 50)
        response = await client.post(
            f"{base_url}/games/search",
            json={"query": "Baldur's Gate 3", "limit": 3},
        )
        search_results = response.json()
        print(json.dumps(search_results, indent=2))
        print()

        # Get first game's app_id
        if search_results:
            app_id = search_results[0].get("app_id")

            if app_id:
                # 3. Get game details
                print("=" * 50)
                print(f"3. Getting details for app_id: {app_id}")
                print("=" * 50)
                response = await client.post(
                    f"{base_url}/games/details", json={"app_id": app_id}
                )
                details = response.json()
                print(f"Name: {details.get('name')}")
                print(f"Release Date: {details.get('release_date')}")
                print(f"Price: {details.get('price')}")
                print(f"Genres: {', '.join(details.get('genres', []))}")
                print()

                # 4. Analyze game sentiment
                print("=" * 50)
                print(f"4. Analyzing game sentiment for {details.get('name')}")
                print("=" * 50)
                response = await client.post(
                    f"{base_url}/games/analyze", json={"app_id": app_id}
                )
                analysis = response.json()
                print(f"Game: {analysis.get('game_name')}")
                print(f"\nAnalysis:\n{analysis.get('analysis', 'N/A')[:500]}...")
                print()

        # 5. Simple chat without tools
        print("=" * 50)
        print("5. Simple Chat (no tools)")
        print("=" * 50)
        response = await client.post(
            f"{base_url}/chat",
            json={
                "message": "¿Qué tipo de consultas puedes responder sobre videojuegos?",
                "use_tools": False,
            },
        )
        chat_response = response.json()
        print(f"Bot: {chat_response.get('response')}")
        print()

        # 6. Chat with tools
        print("=" * 50)
        print("6. Chat with Tools")
        print("=" * 50)
        response = await client.post(
            f"{base_url}/chat",
            json={
                "message": "Busca información sobre Elden Ring y dime qué opinan los jugadores",
                "use_tools": True,
            },
        )
        chat_response = response.json()
        print(f"Bot: {chat_response.get('response')[:500]}...")
        print()

        # 7. Knowledge base stats
        print("=" * 50)
        print("7. Knowledge Base Statistics")
        print("=" * 50)
        response = await client.get(f"{base_url}/knowledge/stats")
        stats = response.json()
        print(json.dumps(stats, indent=2))
        print()

        print("🎉 Examples completed!")


if __name__ == "__main__":
    print("Make sure the API is running on http://localhost:8000\n")
    print("Start with: python -m uvicorn src.main:app --reload\n")

    try:
        asyncio.run(main())
    except httpx.ConnectError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the server is running!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
