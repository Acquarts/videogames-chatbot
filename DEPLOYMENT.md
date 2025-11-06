# 🚀 Guía de Despliegue

Esta guía cubre el despliegue del Videogames Chatbot (Frontend + Backend) en Railway.

## 🎉 Estado Actual

**¡EL PROYECTO YA ESTÁ DESPLEGADO EN RAILWAY!**

- **Frontend**: https://videogames-chatbot-frontend.up.railway.app
- **Backend API**: https://videogames-chatbot-production.up.railway.app
- **Documentación API**: https://videogames-chatbot-production.up.railway.app/docs

## 📋 Tabla de Contenidos

- [Railway (Actualmente en uso)](#railway)
- [Redesplegar cambios](#redesplegar-cambios-en-railway)
- [Variables de Entorno](#variables-de-entorno)
- [Troubleshooting](#troubleshooting)

---

## Railway

Railway es la opción más simple y rápida. **Ya está configurado y funcionando.**

### Arquitectura Actual en Railway

El proyecto está dividido en **dos servicios independientes**:

1. **Backend Service**:
   - Directorio: `backend/`
   - Puerto: 8000
   - URL: https://videogames-chatbot-production.up.railway.app

2. **Frontend Service**:
   - Directorio: `frontend/`
   - Puerto: 3000
   - URL: https://videogames-chatbot-frontend.up.railway.app

### Variables de Entorno Configuradas

#### Backend Service

```env
ANTHROPIC_API_KEY=sk-ant-api03-***  # Claude API Key
ENV=production
DEBUG=False
LOG_LEVEL=INFO
CLAUDE_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
TEMPERATURE=0.7
PORT=8000
```

#### Frontend Service

```env
NEXT_PUBLIC_API_URL=https://videogames-chatbot-production.up.railway.app
```

### Notas Importantes

- **ChromaDB/RAG deshabilitado**: ONNXRuntime tiene problemas de kernel en Railway
- **Redis opcional**: No es crítico, el sistema funciona sin él
- **Steam API Key**: Opcional, la mayoría de funciones trabajan sin ella

## Redesplegar Cambios en Railway

### Opción 1: Automático (Recomendado)

Railway está conectado al repositorio de GitHub. Cualquier push a `main` triggerea un redeploy automático.

```bash
git add .
git commit -m "Update: descripción del cambio"
git push origin main
```

Railway detectará el cambio y redesplegará automáticamente ambos servicios.

### Opción 2: Manual con Railway CLI

```bash
# Instalar Railway CLI (solo primera vez)
npm install -g @railway/cli

# Login
railway login

# Link al proyecto existente
railway link

# Ver servicios disponibles
railway status

# Desplegar backend
cd backend
railway up

# Desplegar frontend
cd ../frontend
railway up
```

### Verificar Deploy

```bash
# Health check del backend
curl https://videogames-chatbot-production.up.railway.app/api/v1/health

# Ver logs del backend
railway logs

# Abrir frontend en el navegador
open https://videogames-chatbot-frontend.up.railway.app
```

### Configuración de Dominio Personalizado (Opcional)

1. En Railway, selecciona el servicio (backend o frontend)
2. Ve a "Settings" → "Domains"
3. Click en "Custom Domain"
4. Agrega tu dominio (ej: `api.tudominio.com` para backend)
5. Configura los registros DNS según las instrucciones de Railway

### Costos Estimados en Railway

Para este proyecto (Frontend + Backend):

- **Backend**: ~$5-10/mes
- **Frontend**: ~$5-8/mes
- **Total estimado**: ~$10-18/mes

Railway incluye:
- $5 de crédito gratis mensual en el plan Hobby
- Escalado automático
- SSL/HTTPS incluido
- Builds automáticos desde GitHub

---

## Variables de Entorno

### Backend (Requeridas)

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx  # API key de Claude (Anthropic)
```

### Backend (Opcionales)

```env
# Application
APP_NAME=videogames-chatbot
ENV=production                    # development | production
DEBUG=False                       # True | False
LOG_LEVEL=INFO                    # DEBUG | INFO | WARNING | ERROR

# Server
HOST=0.0.0.0
PORT=8000

# LLM
CLAUDE_MODEL=claude-sonnet-4-5
MAX_TOKENS=4096
TEMPERATURE=0.7

# Steam API (opcional, funciona sin ella)
STEAM_API_KEY=xxxxx
STEAM_API_BASE_URL=https://api.steampowered.com
STEAM_STORE_API_URL=https://store.steampowered.com/api
```

### Frontend (Requeridas)

```env
NEXT_PUBLIC_API_URL=https://videogames-chatbot-production.up.railway.app
```

En desarrollo local:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## Troubleshooting

### Errores Comunes en Railway

#### 1. Backend Build Failed

**Posibles causas**:
- Dependencias faltantes en `requirements.txt`
- Python version incorrecta

**Solución**:
```bash
# Verifica que requirements.txt esté actualizado
pip freeze > requirements.txt

# Commit y push
git add requirements.txt
git commit -m "Update requirements.txt"
git push origin main
```

#### 2. Frontend Build Failed

**Posibles causas**:
- Dependencias faltantes
- Variables de entorno no configuradas

**Solución**:
1. Verifica que `NEXT_PUBLIC_API_URL` esté configurada en Railway
2. Revisa los logs de Railway
3. Asegúrate de que `package.json` tenga el script de build:
   ```json
   "scripts": {
     "build": "next build",
     "start": "next start"
   }
   ```

#### 3. CORS Errors

**Solución**:
- Verifica que el backend tenga CORS habilitado (ya está configurado en `main.py`)
- Verifica que el frontend use la URL correcta del backend
- En Railway, verifica `NEXT_PUBLIC_API_URL` en las variables de entorno

#### 4. API Returns 500 Errors

**Solución**:
```bash
# Ver logs del backend en Railway
railway logs --service backend

# O desde el dashboard de Railway
# Projects → videogames-chatbot → backend → Deployments → View logs
```

Verifica:
- `ANTHROPIC_API_KEY` está configurada correctamente
- El modelo `claude-sonnet-4-5` es válido
- No hay errores de importación de módulos

#### 5. "Rate limit exceeded" en Steam API

**Solución**:
- Steam limita requests por IP
- El sistema ya tiene caché implementado
- Si el error persiste, considera agregar un Steam API Key en las variables de entorno

### Monitoring y Logs

#### Ver Logs en Railway

```bash
# Desde CLI
railway logs

# Logs específicos del servicio
railway logs --service backend
railway logs --service frontend

# Logs en tiempo real
railway logs --follow
```

#### Desde Railway Dashboard

1. Ve a tu proyecto en Railway
2. Selecciona el servicio (backend o frontend)
3. Click en "Deployments"
4. Click en el deployment activo
5. Ver logs en tiempo real

### Health Checks

#### Backend Health Check

```bash
curl https://videogames-chatbot-production.up.railway.app/api/v1/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

#### Frontend Health Check

Simplemente abre:
```
https://videogames-chatbot-frontend.up.railway.app
```

Deberías ver la interfaz del chatbot.

### Performance Tips

#### 1. Optimizar Tiempos de Respuesta

```env
# En backend .env
CACHE_TTL=7200  # 2 horas para datos de juegos
```

#### 2. Monitorear Uso de Recursos

En Railway Dashboard:
- Metrics → CPU Usage
- Metrics → Memory Usage
- Metrics → Request Volume

Si el uso es alto constantemente, considera:
- Aumentar recursos en Railway (Settings → Resources)
- Optimizar queries a la Steam API
- Implementar más caché

---

## Nuevo Deploy desde Cero

Si necesitas deployar el proyecto a una nueva cuenta de Railway:

### 1. Preparar Repositorio

```bash
# Clonar o tener el repositorio listo
git clone https://github.com/Acquarts/videogames-chatbot.git
cd videogames-chatbot
```

### 2. Crear Proyecto en Railway

1. Ve a [railway.app](https://railway.app)
2. Login con GitHub
3. New Project → Deploy from GitHub repo
4. Selecciona `videogames-chatbot`

### 3. Configurar Backend Service

1. Railway detectará el directorio `backend/`
2. Configura variables de entorno:
   - `ANTHROPIC_API_KEY`
   - `ENV=production`
   - `DEBUG=False`
   - `CLAUDE_MODEL=claude-sonnet-4-5`
3. Railway automáticamente:
   - Detectará `requirements.txt`
   - Instalará dependencias
   - Ejecutará el comando de start

### 4. Configurar Frontend Service

1. Agrega un nuevo servicio al proyecto
2. Selecciona el mismo repositorio
3. Configura el directorio raíz como `frontend/`
4. Configura variables de entorno:
   - `NEXT_PUBLIC_API_URL=<backend-url>` (copia la URL del backend)
5. Railway automáticamente:
   - Detectará `package.json`
   - Ejecutará `npm install`
   - Ejecutará `npm run build`
   - Iniciará con `npm start`

### 5. Verificar Deploy

```bash
# Backend
curl <backend-url>/api/v1/health

# Frontend
open <frontend-url>
```

---

## Soporte

Si tienes problemas:

1. **Revisa los logs en Railway**
   ```bash
   railway logs --follow
   ```

2. **Verifica variables de entorno**
   - Railway Dashboard → Project → Service → Variables

3. **Consulta documentación**:
   - [Railway Docs](https://docs.railway.app/)
   - [FastAPI Docs](https://fastapi.tiangolo.com/)
   - [Next.js Docs](https://nextjs.org/docs)

4. **Abre un issue en GitHub**:
   https://github.com/Acquarts/videogames-chatbot/issues

---

**¡Proyecto desplegado exitosamente!** 🚀
