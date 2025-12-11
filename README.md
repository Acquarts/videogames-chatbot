# 🎮 Videogames Chatbot

Specialized videogames chatbot with Steam API integration, powered by Claude AI and RAG (Retrieval Augmented Generation).

## 🌟 Features

### 🤖 Conversational Intelligence
- **Natural and fluid conversations** - The chatbot has a real gamer personality, not robotic
- **Conversation context** - Remembers and references previous messages
- **Intelligent flexibility** - Can discuss genres, mechanics and trends without needing data
- **Efficient tool usage** - Only queries APIs when it really needs specific data

### 🔧 Chatbot Tools
1. **search_steam_games** - Search games by name or keyword
2. **search_games_by_genre** - Optimized search by genre (horror, indie, RPG, etc.)
3. **get_game_details** - Complete information about a specific game
4. **get_multiple_games_details** - Gets data from multiple games in parallel (perfect for comparisons)
5. **get_game_reviews** - User reviews and satisfaction statistics

### 🎯 Standout Capabilities
- **Game search** on the Steam platform
- **Detailed information** about videogames: description, developers, prices, release dates, etc.
- **Intelligent recommendations** by genre with a single query
- **Efficient comparisons** between multiple games
- **Review analysis** with AI to determine:
  - Satisfaction level
  - Perceived difficulty
  - Originality
  - Artistic quality
  - Most valued and criticized aspects
- **RAG (Retrieval Augmented Generation)** with ChromaDB for contextual memory
- **Intelligent caching** with Redis to optimize performance
- **Robust REST API** with FastAPI
- **Next.js Frontend** with modern and responsive interface
- **Ready to deploy** on Railway with auto-deploy

## 🆕 New Improvements (v2.0)

### ✨ More Natural Conversation
The chatbot now has a more human and conversational personality:
- Talks like a fellow gamer, not like a bot
- Uses occasional emojis for emphasis (🔥, ⭐, 🎮)
- Can discuss general topics without needing tools
- Admits limitations honestly
- Is enthusiastic but critical when data shows it

### ⚡ Optimized Performance
- **Increased iteration limit**: From 5 to 10 for complex queries
- **New specialized tools**:
  - `get_multiple_games_details` for comparisons
  - `search_games_by_genre` for recommendations
- **Fewer API calls**: More efficient tools reduce iterations

### 🎮 Queries That Now Work Perfectly
- ✅ "Recommend indie horror games" → 2-3 iterations (previously failed)
- ✅ "Compare Cyberpunk 2077 with The Witcher 3" → 2-3 iterations (previously failed)
- ✅ "What do you think about souls-like games?" → No tools, direct conversation
- ✅ "Find games similar to Hollow Knight" → Intelligent search with context

## 🏗️ Architecture

```
┌─────────────────┐
│   Frontend      │  Next.js + TypeScript
│  (Next.js)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   User          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI        │
│  (REST API)     │
└────────┬────────┘
         │
    ┌────┴────────────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌──────────┐
│ Claude  │         │ Steam    │
│   AI    │◄───────►│   API    │
└────┬────┘         └──────────┘
     │
     ▼
┌──────────────┐
│  ChromaDB    │
│  (RAG/Vector │
│   Database)  │
└──────────────┘
     │
     ▼
┌──────────────┐
│   Redis      │
│  (Cache)     │
└──────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- Anthropic API Key (Claude) - Required
- Steam API Key (optional, works without it)

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Acquarts/videogames-chatbot.git
cd videogames-chatbot
```

### 2. Get API Keys

#### Steam API Key (Optional)
1. Visit https://steamcommunity.com/dev/apikey
2. Log in with your Steam account
3. Register a domain (you can use `localhost` for development)
4. Copy your API Key

#### Anthropic API Key (Claude) - Required
1. Visit https://console.anthropic.com/
2. Create an account or log in
3. Go to "API Keys" in your dashboard
4. Generate a new API key
5. Copy your API key

### 3. Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your Claude API key:

```env
ANTHROPIC_API_KEY=your_claude_api_key
STEAM_API_KEY=your_steam_api_key  # Optional
```

### 4. Configure Frontend

```bash
cd frontend
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Install and run

**Backend:**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python -m uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend

# Install dependencies
npm install

# Run in development
npm run dev
```

## 📖 API Usage

The API will be available at `http://localhost:8000`

### Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Main Endpoints

#### 1. Chat with the bot

```bash
POST /api/v1/chat
```

```json
{
  "message": "Recommend indie horror games",
  "conversation_history": [],
  "use_tools": true
}
```

#### 2. Search games

```bash
POST /api/v1/games/search
```

```json
{
  "query": "Elden Ring",
  "limit": 10
}
```

#### 3. Get game details

```bash
POST /api/v1/games/details
```

```json
{
  "app_id": 1245620
}
```

#### 4. Analyze game sentiment

```bash
POST /api/v1/games/analyze
```

```json
{
  "app_id": 1245620
}
```

### Examples with cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Search for a game
curl -X POST "http://localhost:8000/api/v1/games/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"Baldurs Gate 3", "limit":5}'

# Chat with the bot
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Compare Cyberpunk 2077 with The Witcher 3",
    "use_tools": true
  }'
```

## 🎨 Frontend

The frontend is built with Next.js 14, TypeScript and Tailwind CSS.

### Features:
- ✅ Modern and responsive chat interface
- ✅ Markdown rendering for bot responses
- ✅ Conversation history
- ✅ Predefined suggestion buttons
- ✅ Loading states and error handling
- ✅ Dark mode support
- ✅ Smooth animations

### Frontend Development:

```bash
cd frontend
npm run dev      # Development
npm run build    # Build for production
npm start        # Production
npm run lint     # Linting
```

## 🚀 Deployment

### Railway (Recommended)

The project is configured to deploy automatically on Railway:

**Backend:**
1. Create a new project on Railway
2. Connect your GitHub repository
3. Railway will detect `backend/` automatically
4. Configure environment variables in Railway
5. Automatic deploy on each push

**Frontend:**
1. Create another service in the same Railway project
2. Configure the root directory: `frontend`
3. Add variable: `NEXT_PUBLIC_API_URL=https://your-backend.railway.app`
4. Automatic deploy

More details in [DEPLOYMENT.md](DEPLOYMENT.md)

## 🛠️ Development

### Project Structure

```
videogames-chatbot/
├── backend/              # FastAPI Backend
│   ├── src/
│   │   ├── api/          # FastAPI Endpoints
│   │   ├── config/       # Configuration
│   │   ├── services/     # Business logic
│   │   │   ├── steam_service.py
│   │   │   ├── rag_service.py
│   │   │   └── chatbot_service.py  # 🆕 Improved with personality
│   │   ├── utils/        # Utilities
│   │   └── main.py       # Entry point
│   └── requirements.txt
│
├── frontend/             # Next.js Frontend
│   ├── app/              # App router
│   ├── components/       # React components
│   ├── lib/              # Utilities
│   └── package.json
│
├── README.md
├── DEPLOYMENT.md
├── QUICKSTART.md
└── PROJECT_SUMMARY.md
```

### Run Tests

```bash
# Backend
cd backend
pytest

# With coverage
pytest --cov=src tests/

# Frontend
cd frontend
npm test
```

### Code Quality

```bash
# Backend - Format code
cd backend
black src/

# Backend - Linting
flake8 src/

# Frontend - Linting
cd frontend
npm run lint
```

## 📊 Technical Features

### Technologies

**Backend:**
- Framework: FastAPI
- LLM: Claude 4.5 Sonnet (Anthropic)
- Orchestration: LangChain
- Vector Database: ChromaDB
- Cache: Redis
- External API: Steam Web API

**Frontend:**
- Framework: Next.js 14
- Language: TypeScript
- Styling: Tailwind CSS
- UI Components: Shadcn/ui
- Markdown: React Markdown

**DevOps:**
- Deployment: Railway (auto-deploy from GitHub)
- Build System: Nixpacks (automatic on Railway)

### Optimizations

- **Multi-level cache**: In-memory cache, ChromaDB for embeddings (currently disabled)
- **Async/await**: Asynchronous operations for better performance
- **Connection pooling**: HTTP connection reuse
- **Rate limiting**: Prevention of API overload
- **Intelligent tool calling**: Reduces iterations and API costs
- **Efficient deployment**: Railway handles builds automatically

### Scalability

- Stateless architecture
- Ready for horizontal replicas
- Persistent vector database
- Compatible with load balancers
- Static frontend optimized with Next.js

## 🔒 Security

- Environment variables for secrets
- Configured health checks
- Input validation with Pydantic
- Error logging and auditing
- Configured CORS
- API key validation
- Secure deployment on Railway with automatic SSL/HTTPS

## 📝 Future Improvements

- [ ] User authentication
- [ ] Webhooks for Steam updates
- [ ] Multi-language support
- [ ] Integration with more platforms (Epic, GOG, etc.)
- [ ] Personalized recommendation system with ML
- [ ] Usage analytics and metrics
- [ ] Mobile app (React Native)
- [ ] Voice interface

## 🤝 Contributions

Contributions are welcome! Please:

1. Fork the project
2. Create a branch for your feature (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is under the MIT license. See `LICENSE` for more information.

## 👤 Author

Adrián - [GitHub](https://github.com/Acquarts)

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude AI
- [Steam](https://steamcommunity.com/dev) for their public API
- [LangChain](https://www.langchain.com/) for the framework
- [ChromaDB](https://www.trychroma.com/) for the vector database
- [Next.js](https://nextjs.org/) for the frontend framework
- [Railway](https://railway.app/) for hosting

---

**Questions or problems?** Open an issue on GitHub.

**Enjoy building with Videogames Chatbot!** 🎮🤖
