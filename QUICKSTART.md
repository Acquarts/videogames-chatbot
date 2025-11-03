# 🚀 Quick Start Guide

Get your Videogames Chatbot up and running in 5 minutes!

## Prerequisites

- Python 3.11 or higher
- API Keys:
  - **Claude API Key**: Get it from [console.anthropic.com](https://console.anthropic.com/)
  - **Steam API Key**: Get it from [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)

## Step 1: Setup

### Windows

```bash
# Run setup script
.\scripts\setup.bat

# Or manually:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac

```bash
# Make script executable
chmod +x scripts/setup.sh

# Run setup script
./scripts/setup.sh

# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Configure API Keys

Edit `.env` file and add your keys:

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx
STEAM_API_KEY=xxxxx
```

## Step 3: Run the Server

```bash
# Development mode (with hot reload)
python -m uvicorn src.main:app --reload

# Or production mode
python -m uvicorn src.main:app
```

Server will start at: **http://localhost:8000**

## Step 4: Test It!

### Option A: Interactive Docs (Recommended)

Open your browser: **http://localhost:8000/docs**

Try the `/api/v1/chat` endpoint:

```json
{
  "message": "¿Cuáles son los mejores juegos de 2024?",
  "use_tools": true
}
```

### Option B: cURL

```bash
# Simple chat
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, ¿qué puedes hacer?", "use_tools": false}'

# Search for games
curl -X POST "http://localhost:8000/api/v1/games/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Elden Ring", "limit": 5}'
```

### Option C: Python Script

```bash
python examples/simple_usage.py
```

## Step 5: Try With Docker (Optional)

```bash
# Development with hot reload
docker-compose -f docker-compose.dev.yml up

# Production
docker-compose up -d
```

## Example Queries

Once the API is running, try these example queries:

### 1. **General Questions**
```json
{
  "message": "¿Qué puedes hacer?",
  "use_tools": false
}
```

### 2. **Search Games**
```json
{
  "message": "Busca juegos de rol japoneses",
  "use_tools": true
}
```

### 3. **Game Analysis**
```json
{
  "message": "¿Qué opinan los jugadores sobre Baldur's Gate 3?",
  "use_tools": true
}
```

### 4. **Game Recommendations**
```json
{
  "message": "Recomiéndame juegos similares a Dark Souls pero más fáciles",
  "use_tools": true
}
```

### 5. **Detailed Information**
```json
{
  "message": "Dame información detallada sobre Elden Ring: fecha de lanzamiento, precio, reseñas y dificultad",
  "use_tools": true
}
```

## Quick API Reference

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Chat with the bot |
| POST | `/api/v1/games/search` | Search games |
| POST | `/api/v1/games/details` | Get game details |
| POST | `/api/v1/games/analyze` | Analyze game sentiment |
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/knowledge/stats` | Knowledge base stats |

### Full Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Troubleshooting

### Issue: "ModuleNotFoundError"

```bash
# Make sure you activated the virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "anthropic_api_key is required"

Make sure your `.env` file has the correct API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

### Issue: "Connection refused" or "Cannot connect to API"

Make sure the server is running:

```bash
python -m uvicorn src.main:app --reload
```

### Issue: "Steam API rate limit exceeded"

Steam limits requests. Wait a moment and try again. The system has caching to reduce API calls.

### Issue: "Port 8000 already in use"

```bash
# Use a different port
python -m uvicorn src.main:app --port 8001
```

## Next Steps

- ✅ Read the full [README.md](README.md)
- ✅ Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- ✅ Explore the API with the interactive docs at `/docs`
- ✅ Try the example script: `python examples/simple_usage.py`

## Need Help?

- Check the logs: `logs/` directory
- Review the documentation: http://localhost:8000/docs
- Open an issue on GitHub

---

**Enjoy building with Videogames Chatbot!** 🎮🤖
