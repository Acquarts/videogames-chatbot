# Videogames Chatbot Frontend

Frontend de Next.js para el chatbot de videojuegos con integración a Steam API.

## 🚀 Deploy Rápido

### Backend ya desplegado en Railway:
✅ **URL**: https://videogames-chatbot-production.up.railway.app

### Desplegar Frontend en Vercel:

1. Ve a https://vercel.com e inicia sesión
2. Click en **"Add New Project"**
3. Import desde GitHub: `Acquarts/videogames-chatbot`
4. Configura el proyecto:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Next.js
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

5. Agrega la variable de entorno:
   ```
   NEXT_PUBLIC_API_URL=https://videogames-chatbot-production.up.railway.app
   ```

6. Click en **Deploy**

¡Listo! Tu frontend estará disponible en una URL de Vercel.

## 🛠️ Desarrollo Local

1. Copia el archivo de ejemplo:
   ```bash
   cp .env.example .env.local
   ```

2. Instala dependencias:
   ```bash
   npm install
   ```

3. Inicia el servidor de desarrollo:
   ```bash
   npm run dev
   ```

4. Abre http://localhost:3000

## 📝 Variables de Entorno

- `.env.local` - Para desarrollo local (no se sube a Git)
- `.env.production` - Para producción (se usa automáticamente en deploy)
- `.env.example` - Plantilla de ejemplo

## 🌐 URLs

- **Backend (Railway)**: https://videogames-chatbot-production.up.railway.app
- **API Docs**: https://videogames-chatbot-production.up.railway.app/docs
- **Frontend**: (se generará después del deploy en Vercel)
