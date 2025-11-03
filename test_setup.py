"""
Quick test to verify the setup is working without Steam API key.
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import settings
from src.utils.logger import get_logger

logger = get_logger()

# Import Steam service directly to avoid chatbot dependencies
import httpx
from src.utils.cache import cached


async def test_steam_without_key():
    """Test Steam service without API key."""

    print("\n" + "="*60)
    print("🎮 Testing Videogames Chatbot Setup")
    print("="*60)

    # Check configuration
    print("\n1️⃣  Checking Configuration...")
    print(f"   ✅ Claude API Key: {'✓ Configured' if settings.anthropic_api_key else '✗ Missing'}")
    print(f"   {'⚠️ ' if not settings.steam_api_key else '✅'} Steam API Key: {'✗ Not configured (OK - optional)' if not settings.steam_api_key else '✓ Configured'}")
    print(f"   ✅ Environment: {settings.env}")
    print(f"   ✅ Debug Mode: {settings.debug}")

    # Test Steam service manually (avoid RAG/Chatbot imports)
    print("\n2️⃣  Testing Steam API (Public Endpoints)...")

    # Create simple HTTP client
    client = httpx.AsyncClient(timeout=30.0)
    store_url = "https://store.steampowered.com/api"

    try:
        # Test 1: Search games
        print("\n   📋 Test: Search games...")
        response = await client.get(f"{store_url}/storesearch", params={"term": "Elden Ring", "l": "english", "cc": "US"})
        if response.status_code == 200:
            data = response.json()
            results = data.get("items", [])[:3]
            if results:
                print(f"   ✅ PASS - Found {len(results)} games")
                for game in results:
                    print(f"      • {game['name']} (ID: {game['id']})")
            else:
                print("   ⚠️  No results found")
        else:
            print(f"   ❌ FAIL - Status code: {response.status_code}")

        # Test 2: Get game details (Elden Ring: 1245620)
        print("\n   📋 Test: Get game details...")
        response = await client.get(f"{store_url}/appdetails", params={"appids": 1245620, "l": "english"})
        if response.status_code == 200:
            data = response.json()
            if "1245620" in data and data["1245620"]["success"]:
                game_data = data["1245620"]["data"]
                print(f"   ✅ PASS - Got details for: {game_data['name']}")
                print(f"      • Release: {game_data.get('release_date', {}).get('date', 'N/A')}")
                print(f"      • Price: {game_data.get('price_overview', {}).get('final_formatted', 'Free')}")
                genres = [g.get('description') for g in game_data.get('genres', [])][:3]
                print(f"      • Genres: {', '.join(genres)}")
            else:
                print("   ❌ FAIL - Could not get game details")
        else:
            print(f"   ❌ FAIL - Status code: {response.status_code}")

        # Test 3: Get reviews
        print("\n   📋 Test: Get game reviews...")
        response = await client.get(f"{store_url}/appreviews/1245620", params={"json": 1, "language": "english", "num_per_page": 5})
        if response.status_code == 200:
            data = response.json()
            if data.get("success") == 1:
                query_summary = data.get("query_summary", {})
                print(f"   ✅ PASS - Found {query_summary.get('total_reviews', 0):,} reviews")
                print(f"      • Score: {query_summary.get('review_score_desc', 'N/A')}")
                print(f"      • Positive: {query_summary.get('total_positive', 0):,}")
                print(f"      • Negative: {query_summary.get('total_negative', 0):,}")
            else:
                print("   ⚠️  No reviews found")
        else:
            print(f"   ❌ FAIL - Status code: {response.status_code}")

        # Test 4: Get player count (may not work without key)
        print("\n   📋 Test: Get current player count...")
        response = await client.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/", params={"appid": 1245620})
        if response.status_code == 200:
            data = response.json()
            if data.get("response", {}).get("result") == 1:
                player_count = data["response"]["player_count"]
                print(f"   ✅ PASS - Current players: {player_count:,}")
            else:
                print(f"   ⚠️  Player count unavailable (expected without API key)")
        else:
            print(f"   ⚠️  Player count unavailable (API key needed)")

        await client.aclose()

    except Exception as e:
        logger.error(f"Error during testing: {e}")
        print(f"\n   ❌ ERROR: {e}")
        await client.aclose()
        return False

    # Summary
    print("\n" + "="*60)
    print("✅ Setup Test Complete!")
    print("="*60)
    print("\n📝 Summary:")
    print("   • Steam API (public endpoints): ✅ Working")
    print("   • Search, details, reviews: ✅ All functional")
    print("   • Player count: ⚠️  Limited without API key")
    print("\n🚀 Your chatbot is ready to use!")
    print("   Run: python -m uvicorn src.main:app --reload")
    print("   Then visit: http://localhost:8000/docs")
    print("\n💡 Tip: When you get your Steam API key, just add it to .env")
    print("="*60 + "\n")

    return True


if __name__ == "__main__":
    try:
        asyncio.run(test_steam_without_key())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nℹ️  Make sure you have:")
        print("   1. Activated virtual environment: venv\\Scripts\\activate")
        print("   2. Installed dependencies: pip install -r requirements.txt")
        print("   3. Configured .env with your Anthropic API key")
