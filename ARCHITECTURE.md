# 🏗️ Architecture Documentation

Complete architecture overview of the Videogames Chatbot system.

## Table of Contents

- [System Overview](#system-overview)
- [Components](#components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Decisions](#design-decisions)
- [Scalability](#scalability)
- [Security](#security)

---

## System Overview

The Videogames Chatbot is a microservices-oriented application that combines:
- **LLM (Claude)** for natural language understanding and generation
- **Steam API** for real-time game data
- **RAG (ChromaDB)** for semantic search and knowledge persistence
- **Redis** for caching and performance optimization

### High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                       Client Layer                        │
│  (HTTP Clients, Web Browsers, Mobile Apps, CLI Tools)    │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│                      API Gateway                          │
│                    FastAPI + Uvicorn                      │
│  ┌────────────┐  ┌─────────────┐  ┌──────────────┐      │
│  │   CORS     │  │  Validation │  │   Logging    │      │
│  │ Middleware │  │  (Pydantic) │  │  Middleware  │      │
│  └────────────┘  └─────────────┘  └──────────────┘      │
└────────────────────┬─────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      │              │              │
      ▼              ▼              ▼
┌───────────┐  ┌────────────┐  ┌───────────┐
│  Chatbot  │  │   Steam    │  │    RAG    │
│  Service  │  │  Service   │  │  Service  │
└─────┬─────┘  └─────┬──────┘  └─────┬─────┘
      │              │                │
      ▼              ▼                ▼
┌───────────┐  ┌────────────┐  ┌───────────┐
│  Claude   │  │ Steam API  │  │ ChromaDB  │
│    AI     │  │  (HTTP)    │  │ (Vector)  │
└───────────┘  └────────────┘  └───────────┘
                     │
                     ▼
              ┌────────────┐
              │   Redis    │
              │  (Cache)   │
              └────────────┘
```

---

## Components

### 1. API Layer (`src/api/`)

**Purpose**: HTTP interface for client interactions

**Files**:
- `routes.py`: API endpoints definition
- `models.py`: Pydantic request/response models
- `__init__.py`: Package initialization

**Responsibilities**:
- Request validation
- Response serialization
- Error handling
- Endpoint routing

**Key Endpoints**:
- `POST /api/v1/chat`: Main chat interface
- `POST /api/v1/games/search`: Search games
- `POST /api/v1/games/details`: Get game information
- `POST /api/v1/games/analyze`: AI-powered sentiment analysis
- `GET /api/v1/health`: Health check

### 2. Configuration Layer (`src/config/`)

**Purpose**: Centralized configuration management

**Files**:
- `settings.py`: Environment variables and configuration

**Features**:
- Environment-based configuration
- Type-safe settings with Pydantic
- Cached settings for performance
- Validation of required parameters

**Key Settings**:
```python
- API Keys (Anthropic, Steam)
- Server configuration (host, port)
- LLM parameters (model, temperature)
- Cache settings (TTL, Redis URL)
- ChromaDB persistence path
```

### 3. Service Layer (`src/services/`)

#### 3.1 Steam Service (`steam_service.py`)

**Purpose**: Integration with Steam Web API

**Key Methods**:
```python
- get_game_details(app_id) → Game information
- get_game_reviews(app_id) → User reviews
- search_games(query) → Search results
- get_player_count(app_id) → Active players
- get_enriched_game_data(app_id) → Combined data
```

**Features**:
- Async HTTP client (httpx)
- Automatic caching (@cached decorator)
- Error handling and retries
- Rate limiting awareness

#### 3.2 RAG Service (`rag_service.py`)

**Purpose**: Knowledge base management with vector search

**Key Methods**:
```python
- add_game_to_knowledge_base(game_data) → Store game info
- search_similar_games(query) → Semantic search
- get_game_context(app_id) → Retrieve stored context
- get_collection_stats() → Knowledge base statistics
```

**Features**:
- Persistent vector storage (ChromaDB)
- Semantic similarity search
- Document embeddings
- Metadata filtering

**Document Types**:
- Game information (structured data)
- User reviews (unstructured text)
- Metadata (app_id, timestamps, types)

#### 3.3 Chatbot Service (`chatbot_service.py`)

**Purpose**: Core LLM orchestration with LangChain

**Key Methods**:
```python
- chat(message, history) → Agent-based response
- simple_chat(message) → Direct LLM response
- analyze_game_sentiment(app_id) → AI analysis
```

**Features**:
- LangChain integration with direct tool calling
- Enhanced conversational personality (gamer-friendly, natural)
- Intelligent tool usage (only when needed for specific data)
- Conversation history management (last 10 messages)
- Agent executor with configurable iterations (10 max)
- Parallel tool execution for efficiency
- Flexible response generation (can discuss general gaming topics without tools)

**Tools Available to Agent** (v2.0 - Optimized):
1. **search_steam_games**: Find games on Steam by name
2. **search_games_by_genre**: Efficient genre-based search (horror, indie, RPG) - Returns top 5 with details
3. **get_game_details**: Get detailed game data for ONE specific game
4. **get_multiple_games_details**: Get data for MULTIPLE games at once (up to 5) - Perfect for comparisons
5. **get_game_reviews**: Get user reviews and sentiment statistics

**Key Improvements**:
- Increased max iterations from 5 to 10 for complex queries
- New specialized tools reduce API calls significantly
- More natural conversation flow with enhanced system prompt

### 4. Utilities Layer (`src/utils/`)

#### 4.1 Logger (`logger.py`)

**Purpose**: Centralized logging

**Features**:
- Colored console output
- File logging in production
- Log rotation (30 days retention)
- Structured logging format

#### 4.2 Cache Manager (`cache.py`)

**Purpose**: Multi-level caching system

**Features**:
- Redis backend (primary)
- In-memory fallback
- TTL management
- Decorator-based caching (@cached)

**Cache Strategy**:
```
Steam game details → 24 hours
Steam reviews → 1 hour
Search results → 1 hour
```

---

## Data Flow

### Example: User asks about a game

```
1. Client Request
   │
   ├→ POST /api/v1/chat
   │  Body: { "message": "Tell me about Elden Ring" }
   │
2. API Layer (FastAPI)
   │
   ├→ Validate request (Pydantic)
   ├→ Log request
   │
3. Chatbot Service
   │
   ├→ Parse user intent with Claude
   ├→ Determine required tools
   │
4. Tool Execution (LangChain Agent)
   │
   ├→ Tool: search_games("Elden Ring")
   │   │
   │   └→ Steam Service
   │       ├→ Check Redis cache
   │       ├→ If miss: API call to Steam
   │       └→ Cache result
   │
   ├→ Tool: get_game_details(1245620)
   │   │
   │   └→ Steam Service
   │       └→ Enrich with reviews + player count
   │
   ├→ Store in RAG (background)
   │   │
   │   └→ RAG Service
   │       └→ ChromaDB.add(game_data, reviews)
   │
5. Response Generation
   │
   ├→ Claude synthesizes information
   ├→ Format response
   │
6. API Response
   │
   └→ JSON: { "response": "...", "success": true }
   │
7. Client receives response
```

---

## Technology Stack

### Backend Framework
- **FastAPI** 0.109+
  - Modern async Python web framework
  - Automatic API documentation
  - Type hints and validation
  - High performance

### LLM & AI
- **Claude 3.5 Sonnet** (Anthropic)
  - Advanced reasoning capabilities
  - 200K context window
  - Tool use / function calling
  - High quality responses

- **LangChain** 0.1+
  - LLM orchestration
  - Agent framework
  - Tool management
  - Prompt templates

### Vector Database
- **ChromaDB** 0.4+
  - Embedded vector database
  - Persistent storage
  - Semantic search
  - No separate server needed

### Caching
- **Redis** 7+
  - In-memory data store
  - Fast key-value access
  - TTL support
  - Optional (fallback to memory)

### HTTP Client
- **httpx**
  - Async HTTP client
  - HTTP/2 support
  - Connection pooling
  - Timeout management

### Deployment
- **Docker**
  - Multi-stage builds
  - Optimized images
  - Container orchestration

- **Uvicorn**
  - ASGI server
  - High performance
  - Production-ready

---

## Design Decisions

### 1. Why FastAPI over Flask?
- ✅ Native async/await support
- ✅ Automatic API documentation
- ✅ Built-in validation with Pydantic
- ✅ Better performance
- ✅ Modern Python features

### 2. Why Claude over GPT-4?
- ✅ Larger context window (200K vs 128K)
- ✅ Better at following instructions
- ✅ Strong reasoning capabilities
- ✅ Competitive pricing
- ✅ Tool use capabilities

### 3. Why ChromaDB?
- ✅ Embedded (no separate server)
- ✅ Easy to deploy
- ✅ Persistent storage
- ✅ Good performance for moderate scale
- ✅ Simple API
- ⚠️ For AWS migration: Consider Pinecone or OpenSearch

### 4. Why RAG and not just API calls?
- ✅ Persistent knowledge
- ✅ Semantic search capabilities
- ✅ Reduces API calls (cost optimization)
- ✅ Historical data access
- ✅ Better context for LLM

### 5. Why Redis is optional?
- ✅ Simpler local development
- ✅ Fallback to in-memory cache
- ✅ Railway/production can easily add it
- ✅ No hard dependency

### 6. Is LangGraph needed?
- ❌ Not initially
- Reason: Adds complexity for simple tool calling
- ✅ Consider later for:
  - Complex multi-step workflows
  - State management between steps
  - Conditional branching logic

---

## Scalability

### Current Architecture (Railway)

**Capacity**: ~10,000 requests/day

- Single instance deployment
- Embedded ChromaDB
- Optional Redis
- Suitable for: MVP, small projects

### Horizontal Scaling (AWS)

**Capacity**: 100,000+ requests/day

**Changes needed**:
```
1. Load Balancer (ALB)
   ├→ Multiple ECS Fargate tasks

2. Shared ChromaDB → Migrate to:
   ├→ Pinecone (managed vector DB)
   └→ Or OpenSearch with vector plugin

3. Redis → ElastiCache
   └→ Shared cache across instances

4. Session affinity (if using conversation history)
   └→ Store in Redis or database
```

**Auto-scaling Configuration**:
```yaml
Min instances: 2
Max instances: 10
Trigger: CPU > 70% or Memory > 80%
Scale-up: +1 instance
Scale-down: -1 instance (cooldown 5 min)
```

### Bottlenecks & Solutions

| Bottleneck | Solution |
|------------|----------|
| Steam API rate limits | Aggressive caching, queue system |
| ChromaDB writes | Batch processing, async writes |
| Claude API latency | Streaming responses, caching |
| Memory usage (embeddings) | External vector DB (Pinecone) |

---

## Security

### API Keys Management
- ✅ Environment variables (never committed)
- ✅ AWS Secrets Manager (production)
- ✅ Validation at startup

### Container Security
- ✅ Non-root user
- ✅ Multi-stage builds
- ✅ Minimal base image (Python slim)
- ✅ No secrets in image layers

### CORS Configuration
- ⚠️ Currently: `allow_origins=["*"]`
- ✅ Production: Specific domains only
- ✅ Credentials: Restricted

### Input Validation
- ✅ Pydantic models for all inputs
- ✅ Length limits on messages
- ✅ Type checking
- ✅ Sanitization

### Rate Limiting
- ⚠️ Not implemented yet
- ✅ Recommended: Add rate limiting middleware
- ✅ Per-IP or per-user limits

### Logging & Monitoring
- ✅ Structured logging
- ✅ Error tracking
- ✅ Health checks
- ⚠️ Add: APM tool (DataDog, New Relic)

---

## Performance Optimization

### Caching Strategy

```
┌─────────────────────┐
│   Request arrives   │
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ Redis Cache? │
    └──────┬───────┘
           │
      ┌────┴────┐
      │  HIT    │  MISS
      ▼         ▼
  ┌────────┐ ┌──────────────┐
  │ Return │ │ ChromaDB?    │
  └────────┘ └──────┬───────┘
                    │
               ┌────┴────┐
               │  HIT    │  MISS
               ▼         ▼
           ┌────────┐ ┌──────────────┐
           │ Return │ │ Steam API    │
           └────────┘ └──────┬───────┘
                             │
                             ▼
                      ┌────────────┐
                      │ Cache &    │
                      │ Store in   │
                      │ ChromaDB   │
                      └────────────┘
```

### Database Optimization
- Batch inserts to ChromaDB
- Appropriate collection indexing
- Limit document size (truncate long reviews)

### Network Optimization
- HTTP/2 with httpx
- Connection pooling
- Async operations
- Timeout configuration

---

## Monitoring & Observability

### Health Checks
```python
GET /api/v1/health
Response:
{
  "status": "healthy",
  "services": {
    "steam_api": true,
    "rag_service": true,
    "chatbot_service": true
  }
}
```

### Metrics to Track
- Request latency (p50, p95, p99)
- Error rates by endpoint
- Cache hit ratio
- Steam API rate limit usage
- LLM token consumption
- ChromaDB query performance

### Logging Levels
```
DEBUG: Detailed diagnostic info
INFO: General informational messages
WARNING: Warning messages
ERROR: Error messages
```

---

## Future Enhancements

### Short Term
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Add more game platforms (Epic, GOG)
- [ ] Streaming responses
- [ ] WebSocket support

### Medium Term
- [ ] Frontend web interface
- [ ] User preferences and history
- [ ] Recommendation engine
- [ ] Multi-language support
- [ ] GraphQL API

### Long Term
- [ ] Microservices architecture
- [ ] Event-driven architecture (Kafka)
- [ ] Real-time Steam data webhooks
- [ ] Machine learning for recommendations
- [ ] Mobile apps (iOS/Android)

---

## Migration Path: Railway → AWS

### Phase 1: Preparation
1. Test Docker image locally
2. Optimize for production
3. Set up AWS infrastructure (IaC with Terraform)
4. Migrate secrets to Secrets Manager

### Phase 2: Database Migration
1. Export ChromaDB data
2. Upload to S3
3. Migrate to Pinecone or OpenSearch
4. Test vector search parity

### Phase 3: Deployment
1. Push image to ECR
2. Create ECS task definition
3. Deploy to ECS Fargate
4. Configure ALB and health checks
5. Set up auto-scaling

### Phase 4: Cutover
1. Blue-green deployment
2. DNS switch
3. Monitor metrics
4. Rollback plan ready

---

**This architecture is designed to be simple to start, easy to maintain, and ready to scale when needed.** 🚀
