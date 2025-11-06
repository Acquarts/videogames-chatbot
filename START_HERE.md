# 🚀 EMPEZAR AQUI - Guia Rapida

## ✅ Estado del Proyecto

**CHATBOT DE VIDEOJUEGOS CON FRONTEND Y BACKEND COMPLETOS - DESPLEGADO EN RAILWAY**

## 🎯 ¿Qué tienes funcionando?

### ✅ BACKEND (FastAPI + Claude Sonnet 4.5):
- **Búsqueda de juegos** en Steam API ✅
- **Información completa** de juegos (precio, fecha, géneros, descripciones) ✅
- **Reseñas y análisis** de usuarios ✅
- **IA conversacional avanzada** (Claude Sonnet 4.5) con 5 herramientas especializadas ✅
- **Contador de jugadores** activos ✅
- **Comparaciones de juegos** (múltiples juegos a la vez) ✅
- **Búsqueda por género** optimizada ✅
- **API REST completa** con documentación automática ✅

### ✅ FRONTEND (Next.js 15 + React 18):
- **Interfaz de chat moderna** con diseño responsive ✅
- **Markdown rendering** para respuestas formateadas ✅
- **Historial de conversación** persistente ✅
- **Scroll automático** y UX optimizada ✅
- **Integración completa** con backend API ✅

### ⚠️ DESHABILITADO (por compatibilidad Railway):
- **ChromaDB/RAG** - Deshabilitado por problemas de kernel con ONNXRuntime en Railway
- **Redis** - Opcional, no crítico

## 📝 Configuración Actual

Tu archivo `.env` está configurado con:
- ✅ **Anthropic API Key** (Claude Sonnet 4.5) - LISTO
- ⚠️ **Steam API Key** - OPCIONAL (la mayoría de funciones trabajan sin ella)

## 🏃 Para Ejecutar AHORA

### Opción A: Usar la versión desplegada (Recomendado)

**Backend API**: https://videogames-chatbot-production.up.railway.app
**Frontend Web**: https://videogames-chatbot-frontend.up.railway.app

¡Ya está funcionando en producción! Solo abre el frontend y empieza a chatear.

### Opción B: Ejecutar localmente

#### Backend:

```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

pip install -r requirements.txt
python -m uvicorn src.main:app --reload
```

Backend corriendo en: http://localhost:8000

#### Frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend corriendo en: http://localhost:3000

### Paso 3: Prueba el chatbot

**Desde el frontend**: Abre http://localhost:3000 y chatea directamente

**Desde la API**: http://localhost:8000/docs - endpoint `/api/v1/chat`:

```json
{
  "message": "Busca información sobre Elden Ring y dime qué opinan los jugadores",
  "conversation_history": []
}
```

## 🧪 Verificar que Funciona

El chatbot en producción ya ha sido probado:

```
✅ Frontend desplegado en Railway
✅ Backend API funcionando
✅ Claude Sonnet 4.5 integrado
✅ Steam API conectada
✅ 5 herramientas de IA funcionando
✅ Conversaciones fluidas y naturales
```

## 📊 Qué Puedes Preguntar

Ejemplos de consultas que el chatbot puede manejar:

```
"Busca Baldur's Gate 3 y dame detalles"
"¿Qué opinan los jugadores sobre Cyberpunk 2077?"
"Recomiéndame juegos similares a Dark Souls"
"Compara Elden Ring con Dark Souls 3"
"Búscame juegos de terror indie"
"¿Qué tan difícil es Sekiro según las reseñas?"
"Dame información sobre Hollow Knight: precio, reseñas y jugadores"
"¿Cuáles son los mejores RPG de acción en Steam?"
```

## ⚡ Solución de Problemas

### Error: "Module not found" (Backend)
```bash
cd backend
pip install -r requirements.txt
```

### Error: "Cannot find module" (Frontend)
```bash
cd frontend
npm install
```

### Error: "Anthropic API key"
- Verifica que tu key esté en `backend/.env`
- Sin espacios ni comillas extras
- Formato: `ANTHROPIC_API_KEY=sk-ant-...`

### Error: "CORS" o "Network Error"
- Asegúrate que el backend esté corriendo en puerto 8000
- El frontend está configurado para conectarse a `http://localhost:8000`
- En producción, verifica las variables de entorno en Railway

### Puerto ocupado
```bash
# Backend en otro puerto
python -m uvicorn src.main:app --port 8001

# Frontend en otro puerto
npm run dev -- -p 3001
```

## 🎮 Steam API Key (Opcional)

La Steam API Key es opcional. La mayoría de funciones trabajan sin ella usando endpoints públicos.

Si quieres agregarla:

1. Obtén tu key en: https://steamcommunity.com/dev/apikey
2. Edita `backend/.env`
3. Descomenta la línea:
   ```env
   STEAM_API_KEY=tu_key_aqui
   ```
4. Reinicia el backend

## 📚 Documentación Completa

- **Guía rápida**: [QUICKSTART.md](QUICKSTART.md)
- **Deploy**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Resumen del proyecto**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

## 🚢 Estado del Deploy

**¡YA ESTÁ DESPLEGADO EN RAILWAY!**

- **Backend**: https://videogames-chatbot-production.up.railway.app
- **Frontend**: https://videogames-chatbot-frontend.up.railway.app

Para redesplegar cambios:

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link al proyecto existente
railway link

# Deploy
railway up
```

## ✨ Proyecto Completo

Tu chatbot incluye:
- ✅ **Frontend moderno** con Next.js 15 y React 18
- ✅ **Backend robusto** con FastAPI y Python 3.11
- ✅ **IA conversacional** con Claude Sonnet 4.5
- ✅ **5 herramientas especializadas** para búsqueda y análisis
- ✅ **Steam API** integrada (funciona sin key)
- ✅ **Desplegado en producción** en Railway
- ✅ **Documentación completa**

**¡ESTÁ FUNCIONANDO EN PRODUCCIÓN!** 🎮🤖

---

**Backend Local**: `cd backend && python -m uvicorn src.main:app --reload`
**Frontend Local**: `cd frontend && npm run dev`
**Producción**: https://videogames-chatbot-frontend.up.railway.app
