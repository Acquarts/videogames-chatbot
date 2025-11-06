# 🚀 Quick Start Guide

Get your Videogames Chatbot up and running in 5 minutes!

## 🌐 Opción 1: Usar la versión en producción (Más Rápido)

**¡Ya está desplegado y funcionando!**

- **Frontend**: https://videogames-chatbot-frontend.up.railway.app
- **Backend API**: https://videogames-chatbot-production.up.railway.app

Solo abre el frontend y empieza a chatear. No necesitas instalar nada.

## 💻 Opción 2: Ejecutar localmente

### Prerequisites

- **Python 3.11** or higher
- **Node.js 18** or higher
- **Anthropic API Key**: Get it from [console.anthropic.com](https://console.anthropic.com/)
- **Steam API Key**: (Opcional) Get it from [steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey)

## Step 1: Setup Backend

### Windows

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux/Mac

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 2: Configure Backend API Keys

Create or edit `backend/.env` file:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-xxxxx

# Optional (most features work without it)
# STEAM_API_KEY=xxxxx

# Application
ENV=development
DEBUG=True
PORT=8000
CLAUDE_MODEL=claude-sonnet-4-5
```

## Step 3: Run Backend Server

```bash
cd backend
python -m uvicorn src.main:app --reload
```

Backend will start at: **http://localhost:8000**

## Step 4: Setup Frontend

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 5: Run Frontend

```bash
cd frontend
npm run dev
```

Frontend will start at: **http://localhost:3000**

## Step 6: Test It!

### Option A: Use the Frontend (Recommended)

Open your browser: **http://localhost:3000**

Start chatting with the bot directly in the beautiful web interface!

### Option B: Test Backend API

Open your browser: **http://localhost:8000/docs**

Try the `/api/v1/chat` endpoint:

```json
{
  "message": "Busca información sobre Elden Ring",
  "conversation_history": []
}
```

### Option C: cURL

```bash
# Chat endpoint
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Qué puedes hacer?", "conversation_history": []}'

# Health check
curl http://localhost:8000/api/v1/health
```

## Example Queries

Once the chatbot is running, try these example queries in the frontend or API:

### 1. **General Questions**
```
"¿Qué puedes hacer?"
"Háblame sobre los juegos souls-like"
```

### 2. **Search Games**
```
"Busca juegos de rol japoneses"
"Encuéntrame juegos de terror indie"
```

### 3. **Game Analysis**
```
"¿Qué opinan los jugadores sobre Baldur's Gate 3?"
"Analiza las reseñas de Cyberpunk 2077"
```

### 4. **Game Comparisons**
```
"Compara Elden Ring con Dark Souls 3"
"¿Cuál es mejor: Sekiro o Bloodborne?"
```

### 5. **Game Recommendations**
```
"Recomiéndame juegos similares a Dark Souls pero más fáciles"
"Dame opciones de RPG de acción con buena historia"
```

### 6. **Detailed Information**
```
"Dame información detallada sobre Elden Ring: fecha, precio, reseñas y dificultad"
"¿Cuántos jugadores tiene Hollow Knight? ¿Vale la pena?"
```

## Quick API Reference

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/chat` | Chat with the bot (main endpoint) |
| GET | `/api/v1/health` | Health check |
| GET | `/` | API info |

### Full Documentation

- **Swagger UI (Local)**: http://localhost:8000/docs
- **ReDoc (Local)**: http://localhost:8000/redoc
- **Swagger UI (Production)**: https://videogames-chatbot-production.up.railway.app/docs

## Troubleshooting

### Backend Issues

#### Issue: "ModuleNotFoundError"

```bash
# Make sure you activated the virtual environment
cd backend
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: "anthropic_api_key is required"

Make sure your `backend/.env` file has the correct API key:

```env
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
```

#### Issue: "Port 8000 already in use"

```bash
python -m uvicorn src.main:app --port 8001
```

### Frontend Issues

#### Issue: "Cannot find module"

```bash
cd frontend
npm install
```

#### Issue: "CORS error" or "Network error"

Make sure:
1. Backend is running on port 8000
2. Frontend `.env.local` has: `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. Restart both servers after config changes

#### Issue: "Port 3000 already in use"

```bash
npm run dev -- -p 3001
```

## Next Steps

- ✅ Try the **production version**: https://videogames-chatbot-frontend.up.railway.app
- ✅ Check [DEPLOYMENT.md](DEPLOYMENT.md) for Railway deployment
- ✅ Explore [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture details
- ✅ Review the API docs: http://localhost:8000/docs

## Need Help?

- Check backend logs in terminal
- Review the API documentation: http://localhost:8000/docs
- Open an issue on GitHub: https://github.com/Acquarts/videogames-chatbot

---

**Enjoy chatting about videogames!** 🎮🤖
