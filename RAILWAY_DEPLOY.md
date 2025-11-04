# Deploy en Railway - Guía Simple

## Estructura del Proyecto

```
videogames-chatbot/
├── backend/           # API FastAPI (Python)
│   ├── app.py
│   ├── src/
│   ├── requirements.txt
│   └── railway.json
└── frontend/          # Next.js (React)
    ├── app/
    ├── components/
    └── package.json
```

## Pasos para Deploy

### 1. Crear Proyecto en Railway

1. Ve a [Railway](https://railway.app)
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Conecta este repositorio

### 2. Configurar Backend

Railway detectará automáticamente la carpeta `backend/` como un servicio Python.

**Variables de entorno necesarias:**
- `ANTHROPIC_API_KEY` - Tu API key de Anthropic/Claude
- `PORT` - Railway lo asigna automáticamente

### 3. Configurar Frontend

Railway detectará automáticamente la carpeta `frontend/` como un servicio Next.js.

**Variables de entorno necesarias:**
- `NEXT_PUBLIC_API_URL` - URL del backend (ejemplo: `https://tu-backend.railway.app`)

### 4. Conectar Frontend con Backend

1. Una vez deployado el backend, copia su URL pública
2. En el servicio frontend, agrega la variable `NEXT_PUBLIC_API_URL` con esa URL
3. Redeploy el frontend

## Archivos Eliminados

Se han eliminado los siguientes archivos innecesarios:
- ✅ Todos los archivos Docker (Dockerfile, docker-compose, etc.)
- ✅ Configuraciones duplicadas de Railway
- ✅ Archivos de testing (test_*.py)
- ✅ Carpetas examples/ y scripts/
- ✅ Archivos de configuración innecesarios

## Estructura Simplificada

Railway ahora puede detectar automáticamente:
- **Backend**: Carpeta `backend/` con Python/FastAPI
- **Frontend**: Carpeta `frontend/` con Next.js

No necesitas Docker ni configuraciones complejas. Railway usa **Nixpacks** para detectar y buildear automáticamente cada servicio.

## Verificación

Después del deploy:
1. Backend debe estar en: `https://tu-backend.railway.app/health`
2. Frontend debe estar en: `https://tu-frontend.railway.app`
3. El frontend debe poder comunicarse con el backend

## Notas Importantes

- **ChromaDB está deshabilitado** en el backend actual por incompatibilidades con Railway
- Las dependencias están optimizadas para producción
- El backend usa Uvicorn como servidor ASGI
- El frontend usa Next.js con configuración optimizada
