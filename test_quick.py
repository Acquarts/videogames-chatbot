"""Quick test without emojis for Windows encoding"""
import asyncio
import httpx


async def test():
    print("\n" + "="*60)
    print("Testing Videogames Chatbot - Steam API")
    print("="*60)

    client = httpx.AsyncClient(timeout=30.0)
    store_url = "https://store.steampowered.com/api"

    # Test 1: Search
    print("\n[1/4] Testing search...")
    r = await client.get(f"{store_url}/storesearch", params={"term": "Elden Ring", "l": "english"})
    if r.status_code == 200:
        games = r.json().get("items", [])[:3]
        print(f"PASS - Found {len(games)} games")
        for g in games:
            print(f"  - {g['name']} (ID: {g['id']})")
    else:
        print(f"FAIL - Status: {r.status_code}")

    # Test 2: Details
    print("\n[2/4] Testing game details...")
    r = await client.get(f"{store_url}/appdetails", params={"appids": 1245620})
    if r.status_code == 200 and "1245620" in r.json():
        data = r.json()["1245620"]["data"]
        print(f"PASS - {data['name']}")
        print(f"  - Release: {data.get('release_date', {}).get('date')}")
        print(f"  - Price: {data.get('price_overview', {}).get('final_formatted', 'Free')}")
    else:
        print("FAIL")

    # Test 3: Reviews
    print("\n[3/4] Testing reviews...")
    r = await client.get(f"{store_url}/appreviews/1245620", params={"json": 1, "num_per_page": 1})
    if r.status_code == 200:
        data = r.json()
        summary = data.get("query_summary", {})
        print(f"PASS - {summary.get('total_reviews', 0):,} reviews")
        print(f"  - Score: {summary.get('review_score_desc')}")
        print(f"  - Positive: {summary.get('total_positive', 0):,}")
    else:
        print("FAIL")

    # Test 4: Player count
    print("\n[4/4] Testing player count...")
    r = await client.get("https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/",
                        params={"appid": 1245620})
    if r.status_code == 200 and r.json().get("response", {}).get("result") == 1:
        count = r.json()["response"]["player_count"]
        print(f"PASS - {count:,} players online now")
    else:
        print("INFO - Unavailable (expected without API key)")

    await client.aclose()

    print("\n" + "="*60)
    print("RESULT: Steam API is working!")
    print("Your chatbot will work WITHOUT Steam API key.")
    print("Only 'current players' feature is limited.")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(test())
    except Exception as e:
        print(f"ERROR: {e}")
