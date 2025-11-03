# 🎮 Videogames Chatbot

Chatbot especializado en videojuegos con integración a Steam API, powered by Claude AI y RAG (Retrieval Augmented Generation).

## 🌟 Características

- **Búsqueda de juegos** en la plataforma Steam
- **Información detallada** sobre videojuegos: descripción, desarrolladores, precios, fechas de lanzamiento, etc.
- **Análisis de reseñas** con IA para determinar:
  - Nivel de satisfacción
  - Dificultad percibida
  - Originalidad
  - Calidad artística
  - Aspectos más valorados y criticados
- **RAG (Retrieval Augmented Generation)** con ChromaDB para memoria contextual
- **Caché inteligente** con Redis para optimizar rendimiento
- **API REST** robusta con FastAPI
- **Dockerizado** y listo para desplegar en Railway o AWS

## 🏗️ Arquitectura

```
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
- Docker & Docker Compose (opcional pero recomendado)
- API Key de Anthropic (Claude)
- API Key de Steam

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repo-url>
cd videogames-chatbot
```

### 2. Obtener API Keys

#### Steam API Key
1. Visita https://steamcommunity.com/dev/apikey
2. Inicia sesión con tu cuenta de Steam
3. Registra un dominio (puedes usar `localhost` para desarrollo)
4. Copia tu API Key

#### Anthropic API Key (Claude)
1. Visita https://console.anthropic.com/
2. Crea una cuenta o inicia sesión
3. Ve a "API Keys" en tu dashboard
4. Genera una nueva API key
5. Copia tu API key

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y agrega tus API keys:

```env
ANTHROPIC_API_KEY=tu_api_key_de_claude
STEAM_API_KEY=tu_api_key_de_steam
```

### 4. Instalar dependencias

#### Opción A: Con Docker (Recomendado)

```bash
# Desarrollo con hot reload
docker-compose -f docker-compose.dev.yml up

# Producción
docker-compose up -d
```

#### Opción B: Local con Python

```bash
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
  "message": "¿Cuáles son los mejores juegos de estrategia de 2024?",
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
    "message": "¿Qué opina la gente sobre Baldurs Gate 3?",
    "use_tools": true
  }'
```

## 🚀 Despliegue

### Railway

1. **Crear proyecto en Railway**
   ```bash
   # Instalar Railway CLI
   npm install -g @railway/cli

   # Login
   railway login

   # Iniciar proyecto
   railway init
   ```

2. **Configurar variables de entorno en Railway**
   - Ve a tu proyecto en https://railway.app
   - Settings → Variables
   - Agrega todas las variables de `.env`

3. **Desplegar**
   ```bash
   railway up
   ```

### AWS (ECS/Fargate)

El proyecto está preparado para AWS con las siguientes configuraciones:

```bash
# Build imagen
docker build -t videogames-chatbot .

# Tag para ECR
docker tag videogames-chatbot:latest <tu-ecr-repo>:latest

# Push a ECR
docker push <tu-ecr-repo>:latest

# Desplegar usando ECS/Fargate (requiere configuración adicional de AWS)
```

## 🛠️ Desarrollo

### Estructura del Proyecto

```
videogames-chatbot/
├── src/
│   ├── api/              # Endpoints de FastAPI
│   │   ├── models.py     # Modelos Pydantic
│   │   └── routes.py     # Rutas de la API
│   ├── config/           # Configuración
│   │   └── settings.py   # Variables de entorno
│   ├── services/         # Lógica de negocio
│   │   ├── steam_service.py      # Integración Steam API
│   │   ├── rag_service.py        # Sistema RAG con ChromaDB
│   │   └── chatbot_service.py    # Servicio principal con Claude
│   ├── utils/            # Utilidades
│   │   ├── logger.py     # Sistema de logging
│   │   └── cache.py      # Gestión de caché
│   └── main.py           # Punto de entrada
├── chroma_db/            # Base de datos vectorial (generado)
├── logs/                 # Logs de aplicación (generado)
├── tests/                # Tests unitarios
├── .env.example          # Ejemplo de variables de entorno
├── .gitignore
├── Dockerfile            # Dockerfile multi-stage
├── docker-compose.yml    # Compose para producción
├── docker-compose.dev.yml # Compose para desarrollo
├── railway.json          # Configuración Railway
├── requirements.txt      # Dependencias Python
└── README.md
```

### Ejecutar Tests

```bash
# Con pytest
pytest

# Con cobertura
pytest --cov=src tests/
```

### Código de Calidad

```bash
# Formatear código
black src/

# Linting
flake8 src/
```

## 📊 Características Técnicas

### Tecnologías

- **Framework**: FastAPI
- **LLM**: Claude 3.5 Sonnet (Anthropic)
- **Orquestación**: LangChain
- **Vector Database**: ChromaDB
- **Cache**: Redis
- **API Externa**: Steam Web API
- **Containerización**: Docker

### Optimizaciones

- **Caché multinivel**: Redis para API calls, ChromaDB para embeddings
- **Dockerfile multi-stage**: Imagen optimizada ~200MB
- **Async/await**: Operaciones asíncronas para mejor rendimiento
- **Connection pooling**: Reutilización de conexiones HTTP
- **Rate limiting**: Prevención de sobrecarga de APIs

### Escalabilidad

- Arquitectura sin estado (stateless)
- Preparado para réplicas horizontales
- Base de datos vectorial persistente
- Compatible con load balancers
- Preparado para migración a AWS

## 🔒 Seguridad

- Variables de entorno para secrets
- Usuario no-root en Docker
- Health checks configurados
- Validación de inputs con Pydantic
- Logging de errores y auditoría

## 📝 Próximas Mejoras

- [ ] Frontend web con React/Vue
- [ ] Autenticación de usuarios
- [ ] Webhooks para actualizaciones de Steam
- [ ] Soporte para múltiples idiomas
- [ ] Integración con más plataformas (Epic, GOG, etc.)
- [ ] Sistema de recomendaciones personalizado
- [ ] Analytics y métricas de uso

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

Tu Nombre

## 🙏 Agradecimientos

- [Anthropic](https://www.anthropic.com/) por Claude AI
- [Steam](https://steamcommunity.com/dev) por su API pública
- [LangChain](https://www.langchain.com/) por el framework
- [ChromaDB](https://www.trychroma.com/) por la base de datos vectorial

---

**¿Preguntas o problemas?** Abre un issue en GitHub.
