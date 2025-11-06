# 🎮 Videogames Chatbot

Chatbot especializado en videojuegos con integración a Steam API, powered by Claude AI y RAG (Retrieval Augmented Generation).

## 🌟 Características

### 🤖 Inteligencia Conversacional
- **Conversaciones naturales y fluidas** - El chatbot tiene una personalidad gamer real, no robótica
- **Contexto de conversación** - Recuerda y referencia mensajes anteriores
- **Flexibilidad inteligente** - Puede discutir géneros, mecánicas y tendencias sin necesitar datos
- **Uso eficiente de herramientas** - Solo consulta APIs cuando realmente necesita datos específicos

### 🔧 Herramientas del Chatbot
1. **search_steam_games** - Busca juegos por nombre o palabra clave
2. **search_games_by_genre** - Búsqueda optimizada por género (horror, indie, RPG, etc.)
3. **get_game_details** - Información completa de un juego específico
4. **get_multiple_games_details** - Obtiene datos de múltiples juegos en paralelo (perfecto para comparaciones)
5. **get_game_reviews** - Reseñas de usuarios y estadísticas de satisfacción

### 🎯 Capacidades Destacadas
- **Búsqueda de juegos** en la plataforma Steam
- **Información detallada** sobre videojuegos: descripción, desarrolladores, precios, fechas de lanzamiento, etc.
- **Recomendaciones inteligentes** por género con una sola consulta
- **Comparaciones eficientes** entre múltiples juegos
- **Análisis de reseñas** con IA para determinar:
  - Nivel de satisfacción
  - Dificultad percibida
  - Originalidad
  - Calidad artística
  - Aspectos más valorados y criticados
- **RAG (Retrieval Augmented Generation)** con ChromaDB para memoria contextual
- **Caché inteligente** con Redis para optimizar rendimiento
- **API REST** robusta con FastAPI
- **Frontend Next.js** con interfaz moderna y responsive
- **Dockerizado** y listo para desplegar en Railway

## 🆕 Nuevas Mejoras (v2.0)

### ✨ Conversación Más Natural
El chatbot ahora tiene una personalidad más humana y conversacional:
- Habla como un compañero gamer, no como un bot
- Usa emojis ocasionales para énfasis (🔥, ⭐, 🎮)
- Puede discutir temas generales sin necesitar herramientas
- Admite limitaciones honestamente
- Es entusiasta pero crítico cuando los datos lo muestran

### ⚡ Rendimiento Optimizado
- **Límite de iteraciones aumentado**: De 5 a 10 para consultas complejas
- **Nuevas herramientas especializadas**:
  - `get_multiple_games_details` para comparaciones
  - `search_games_by_genre` para recomendaciones
- **Menos llamadas a API**: Herramientas más eficientes reducen iteraciones

### 🎮 Consultas que Ahora Funcionan Perfectamente
- ✅ "Recomiéndame juegos de terror indie" → 2-3 iteraciones (antes fallaba)
- ✅ "Compara Cyberpunk 2077 con The Witcher 3" → 2-3 iteraciones (antes fallaba)
- ✅ "¿Qué opinas de los souls-like?" → Sin herramientas, conversación directa
- ✅ "Busca juegos parecidos a Hollow Knight" → Búsqueda inteligente con contexto

## 🏗️ Arquitectura

```
┌─────────────────┐
│   Frontend      │  Next.js + TypeScript
│  (Next.js)      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Usuario       │
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

## 📋 Requisitos Previos

- Python 3.11+
- Node.js 18+ (para frontend)
- Docker & Docker Compose (opcional pero recomendado)
- API Key de Anthropic (Claude)
- API Key de Steam (opcional, funciona sin ella)

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/Acquarts/videogames-chatbot.git
cd videogames-chatbot
```

### 2. Obtener API Keys

#### Steam API Key (Opcional)
1. Visita https://steamcommunity.com/dev/apikey
2. Inicia sesión con tu cuenta de Steam
3. Registra un dominio (puedes usar `localhost` para desarrollo)
4. Copia tu API Key

#### Anthropic API Key (Claude) - Requerida
1. Visita https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en tu dashboard
4. Genera una nueva API key
5. Copia tu API key

### 3. Configurar Backend

```bash
cd backend
cp .env.example .env
```

Edita `.env` y agrega tu API key de Claude:

```env
ANTHROPIC_API_KEY=tu_api_key_de_claude
STEAM_API_KEY=tu_api_key_de_steam  # Opcional
```

### 4. Configurar Frontend

```bash
cd frontend
cp .env.local.example .env.local
```

Edita `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Instalar dependencias

#### Opción A: Con Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker-compose up -d
```

Frontend: http://localhost:3000
Backend: http://localhost:8000
API Docs: http://localhost:8000/docs

#### Opción B: Local con Python y Node.js

**Backend:**
```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar aplicación
python -m uvicorn src.main:app --reload
```

**Frontend:**
```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

## 📖 Uso de la API

La API estará disponible en `http://localhost:8000`

### Documentación interactiva

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints Principales

#### 1. Chat con el bot

```bash
POST /api/v1/chat
```

```json
{
  "message": "Recomiéndame juegos de terror indie",
  "conversation_history": [],
  "use_tools": true
}
```

#### 2. Buscar juegos

```bash
POST /api/v1/games/search
```

```json
{
  "query": "Elden Ring",
  "limit": 10
}
```

#### 3. Obtener detalles de un juego

```bash
POST /api/v1/games/details
```

```json
{
  "app_id": 1245620
}
```

#### 4. Analizar sentimiento de un juego

```bash
POST /api/v1/games/analyze
```

```json
{
  "app_id": 1245620
}
```

### Ejemplos con cURL

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Buscar un juego
curl -X POST "http://localhost:8000/api/v1/games/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"Baldurs Gate 3", "limit":5}'

# Chat con el bot
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Compara Cyberpunk 2077 con The Witcher 3",
    "use_tools": true
  }'
```

## 🎨 Frontend

El frontend está construido con Next.js 14, TypeScript y Tailwind CSS.

### Características:
- ✅ Chat interface moderna y responsive
- ✅ Markdown rendering para respuestas del bot
- ✅ Historial de conversación
- ✅ Botones de sugerencias predefinidas
- ✅ Loading states y error handling
- ✅ Dark mode support
- ✅ Animaciones fluidas

### Desarrollo del Frontend:

```bash
cd frontend
npm run dev      # Development
npm run build    # Build para producción
npm start        # Producción
npm run lint     # Linting
```

## 🚀 Despliegue

### Railway (Recomendado)

El proyecto está configurado para desplegarse automáticamente en Railway:

**Backend:**
1. Crea un nuevo proyecto en Railway
2. Conecta tu repositorio de GitHub
3. Railway detectará `backend/` automáticamente
4. Configura las variables de entorno en Railway
5. Deploy automático en cada push

**Frontend:**
1. Crea otro servicio en el mismo proyecto Railway
2. Configura el root directory: `frontend`
3. Agrega variable: `NEXT_PUBLIC_API_URL=https://tu-backend.railway.app`
4. Deploy automático

### Docker Compose

```bash
# Producción
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
videogames-chatbot/
├── backend/              # Backend FastAPI
│   ├── src/
│   │   ├── api/          # Endpoints de FastAPI
│   │   ├── config/       # Configuración
│   │   ├── services/     # Lógica de negocio
│   │   │   ├── steam_service.py
│   │   │   ├── rag_service.py
│   │   │   └── chatbot_service.py  # 🆕 Mejorado con personalidad
│   │   ├── utils/        # Utilidades
│   │   └── main.py       # Punto de entrada
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/             # Frontend Next.js
│   ├── app/              # App router
│   ├── components/       # React components
│   ├── lib/              # Utilities
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── README.md
└── DEPLOYMENT.md
```

### Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Con cobertura
pytest --cov=src tests/

# Frontend
cd frontend
npm test
```

### Código de Calidad

```bash
# Backend - Formatear código
cd backend
black src/

# Backend - Linting
flake8 src/

# Frontend - Linting
cd frontend
npm run lint
```

## 📊 Características Técnicas

### Tecnologías

**Backend:**
- Framework: FastAPI
- LLM: Claude 3.5 Sonnet (Anthropic)
- Orquestación: LangChain
- Vector Database: ChromaDB
- Cache: Redis
- API Externa: Steam Web API

**Frontend:**
- Framework: Next.js 14
- Language: TypeScript
- Styling: Tailwind CSS
- UI Components: Shadcn/ui
- Markdown: React Markdown

**DevOps:**
- Containerización: Docker
- Deployment: Railway
- CI/CD: GitHub Actions (opcional)

### Optimizaciones

- **Caché multinivel**: Redis para API calls, ChromaDB para embeddings
- **Dockerfile multi-stage**: Imagen optimizada ~200MB (backend), ~300MB (frontend)
- **Async/await**: Operaciones asíncronas para mejor rendimiento
- **Connection pooling**: Reutilización de conexiones HTTP
- **Rate limiting**: Prevención de sobrecarga de APIs
- **Tool calling inteligente**: Reduce iteraciones y costos de API

### Escalabilidad

- Arquitectura sin estado (stateless)
- Preparado para réplicas horizontales
- Base de datos vectorial persistente
- Compatible con load balancers
- Frontend estático optimizado con Next.js

## 🔒 Seguridad

- Variables de entorno para secrets
- Usuario no-root en Docker
- Health checks configurados
- Validación de inputs con Pydantic
- Logging de errores y auditoría
- CORS configurado
- API key validation

## 📝 Próximas Mejoras

- [ ] Autenticación de usuarios
- [ ] Webhooks para actualizaciones de Steam
- [ ] Soporte para múltiples idiomas
- [ ] Integración con más plataformas (Epic, GOG, etc.)
- [ ] Sistema de recomendaciones personalizado con ML
- [ ] Analytics y métricas de uso
- [ ] Mobile app (React Native)
- [ ] Voice interface

## 🤝 Contribuciones

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver `LICENSE` para más información.

## 👤 Autor

Adrián - [GitHub](https://github.com/Acquarts)

## 🙏 Agradecimientos

- [Anthropic](https://www.anthropic.com/) por Claude AI
- [Steam](https://steamcommunity.com/dev) por su API pública
- [LangChain](https://www.langchain.com/) por el framework
- [ChromaDB](https://www.trychroma.com/) por la base de datos vectorial
- [Next.js](https://nextjs.org/) por el framework frontend
- [Railway](https://railway.app/) por el hosting

---

**¿Preguntas o problemas?** Abre un issue en GitHub.

**¡Disfruta construyendo con Videogames Chatbot!** 🎮🤖