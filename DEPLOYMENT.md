# 🚀 Guía de Despliegue

Esta guía cubre el despliegue del Videogames Chatbot en diferentes plataformas.

## 📋 Tabla de Contenidos

- [Railway (Recomendado para empezar)](#railway)
- [AWS ECS/Fargate (Para producción enterprise)](#aws-ecsfargate)
- [Variables de Entorno](#variables-de-entorno)
- [Troubleshooting](#troubleshooting)

---

## Railway

Railway es la opción más simple y rápida para desplegar el chatbot.

### Requisitos

- Cuenta en [Railway.app](https://railway.app)
- Repository en GitHub
- API Keys (Steam y Anthropic)

### Paso a Paso

#### 1. Preparar el Repositorio

```bash
# Asegúrate de que todos los archivos estén commiteados
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

#### 2. Crear Proyecto en Railway

**Opción A: Desde la Web**

1. Ve a [railway.app](https://railway.app) y haz login
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Autoriza Railway para acceder a tu GitHub
5. Selecciona el repositorio `videogames-chatbot`
6. Railway detectará automáticamente el `Dockerfile`

**Opción B: Desde CLI**

```bash
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Inicializar proyecto
railway init

# Linkear con proyecto existente o crear nuevo
railway link
```

#### 3. Configurar Variables de Entorno

En el dashboard de Railway:

1. Ve a tu proyecto
2. Click en "Variables"
3. Agrega las siguientes variables:

```env
ANTHROPIC_API_KEY=your_claude_api_key_here
STEAM_API_KEY=your_steam_api_key_here
ENV=production
DEBUG=False
LOG_LEVEL=INFO
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7
PORT=8000
```

#### 4. Agregar Redis (Opcional pero recomendado)

1. En tu proyecto de Railway, click en "+ New"
2. Selecciona "Database" → "Redis"
3. Railway creará automáticamente la variable `REDIS_URL`

#### 5. Desplegar

**Desde Web:**
Railway desplegará automáticamente al hacer push a la rama configurada.

**Desde CLI:**
```bash
railway up
```

#### 6. Verificar Despliegue

```bash
# Obtener URL de la aplicación
railway domain

# Verificar logs
railway logs

# Test de health check
curl https://tu-app.railway.app/api/v1/health
```

### Configuración de Dominio Personalizado

1. En Railway, ve a "Settings" → "Domains"
2. Click en "Custom Domain"
3. Agrega tu dominio
4. Configura los registros DNS según las instrucciones

### Costos Estimados en Railway

- **Starter**: Gratis hasta $5 de uso
- **Developer**: ~$5-20/mes (incluye $5 de crédito)
- **Team**: ~$20-100/mes (dependiendo del uso)

Estimación para este proyecto:
- App (1 instancia): ~$5-10/mes
- Redis: ~$2-3/mes
- **Total: ~$7-13/mes**

---

## AWS ECS/Fargate

Para despliegues de producción con alto tráfico y necesidad de escalabilidad.

### Requisitos

- Cuenta de AWS
- AWS CLI configurado
- Docker instalado localmente
- Terraform o CloudFormation (opcional)

### Arquitectura AWS

```
┌─────────────┐
│  Route 53   │  (DNS)
└──────┬──────┘
       │
┌──────▼──────┐
│     ALB     │  (Load Balancer)
└──────┬──────┘
       │
┌──────▼──────────────┐
│   ECS Fargate       │
│  ┌──────────────┐   │
│  │ Container 1  │   │
│  │ Container 2  │   │
│  └──────────────┘   │
└──────┬──────────────┘
       │
┌──────▼──────┐
│ ElastiCache │  (Redis)
│   (Redis)   │
└─────────────┘
       │
┌──────▼──────┐
│     S3      │  (Chroma DB backups)
└─────────────┘
```

### Paso a Paso

#### 1. Crear repositorio ECR

```bash
# Crear repositorio
aws ecr create-repository --repository-name videogames-chatbot

# Login a ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### 2. Build y Push de la Imagen

```bash
# Build
docker build -t videogames-chatbot .

# Tag
docker tag videogames-chatbot:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/videogames-chatbot:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/videogames-chatbot:latest
```

#### 3. Crear Cluster ECS

```bash
aws ecs create-cluster --cluster-name videogames-chatbot-cluster
```

#### 4. Crear Task Definition

Crea un archivo `task-definition.json`:

```json
{
  "family": "videogames-chatbot",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "videogames-chatbot",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/videogames-chatbot:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "ENV", "value": "production"},
        {"name": "DEBUG", "value": "False"},
        {"name": "LOG_LEVEL", "value": "INFO"}
      ],
      "secrets": [
        {
          "name": "ANTHROPIC_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account-id:secret:anthropic-key"
        },
        {
          "name": "STEAM_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:region:account-id:secret:steam-key"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/videogames-chatbot",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

Registrar task:

```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### 5. Configurar Secrets Manager

```bash
# Guardar API keys en Secrets Manager
aws secretsmanager create-secret \
    --name anthropic-api-key \
    --secret-string "your_claude_api_key"

aws secretsmanager create-secret \
    --name steam-api-key \
    --secret-string "your_steam_api_key"
```

#### 6. Crear ElastiCache (Redis)

```bash
aws elasticache create-cache-cluster \
    --cache-cluster-id videogames-chatbot-cache \
    --cache-node-type cache.t3.micro \
    --engine redis \
    --num-cache-nodes 1
```

#### 7. Crear Application Load Balancer

```bash
# Crear Load Balancer
aws elbv2 create-load-balancer \
    --name videogames-chatbot-alb \
    --subnets subnet-xxxx subnet-yyyy \
    --security-groups sg-xxxx

# Crear Target Group
aws elbv2 create-target-group \
    --name videogames-chatbot-tg \
    --protocol HTTP \
    --port 8000 \
    --vpc-id vpc-xxxx \
    --target-type ip \
    --health-check-path /api/v1/health
```

#### 8. Crear ECS Service

```bash
aws ecs create-service \
    --cluster videogames-chatbot-cluster \
    --service-name videogames-chatbot-service \
    --task-definition videogames-chatbot:1 \
    --desired-count 2 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxx,subnet-yyyy],securityGroups=[sg-xxxx],assignPublicIp=ENABLED}" \
    --load-balancers "targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=videogames-chatbot,containerPort=8000"
```

#### 9. Configurar Auto Scaling

```bash
# Registrar target
aws application-autoscaling register-scalable-target \
    --service-namespace ecs \
    --resource-id service/videogames-chatbot-cluster/videogames-chatbot-service \
    --scalable-dimension ecs:service:DesiredCount \
    --min-capacity 2 \
    --max-capacity 10

# Crear policy de scaling
aws application-autoscaling put-scaling-policy \
    --service-namespace ecs \
    --resource-id service/videogames-chatbot-cluster/videogames-chatbot-service \
    --scalable-dimension ecs:service:DesiredCount \
    --policy-name cpu-scaling-policy \
    --policy-type TargetTrackingScaling \
    --target-tracking-scaling-policy-configuration file://scaling-policy.json
```

### Costos Estimados en AWS

Para tráfico moderado (~10,000 requests/día):

- **Fargate** (2 tasks, 0.5 vCPU, 1GB): ~$30-40/mes
- **ALB**: ~$20-25/mes
- **ElastiCache** (t3.micro): ~$15/mes
- **Data Transfer**: ~$5-10/mes
- **CloudWatch Logs**: ~$5/mes
- **Secrets Manager**: ~$0.80/mes
- **ECR**: ~$1/mes

**Total estimado: ~$75-100/mes**

Para escalar a 100,000+ requests/día: ~$300-500/mes

---

## Variables de Entorno

### Requeridas

```env
ANTHROPIC_API_KEY=sk-ant-xxxxx  # API key de Claude (Anthropic)
STEAM_API_KEY=xxxxx              # API key de Steam
```

### Opcionales

```env
# Application
APP_NAME=videogames-chatbot
ENV=production                    # development | production
DEBUG=False                       # True | False
LOG_LEVEL=INFO                    # DEBUG | INFO | WARNING | ERROR

# Server
HOST=0.0.0.0
PORT=8000                        # Railway usa $PORT automáticamente

# LLM
CLAUDE_MODEL=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
TEMPERATURE=0.7

# ChromaDB
CHROMA_PERSIST_DIR=./chroma_db

# Redis (opcional)
REDIS_URL=redis://localhost:6379
CACHE_TTL=3600

# Steam API
STEAM_API_BASE_URL=https://api.steampowered.com
STEAM_STORE_API_URL=https://store.steampowered.com/api
```

---

## Troubleshooting

### Errores Comunes

#### 1. "ChromaDB collection not found"

**Solución:**
```bash
# Asegúrate de que el directorio chroma_db tenga permisos correctos
chmod -R 755 chroma_db

# O en Docker, monta el volumen correctamente
docker run -v $(pwd)/chroma_db:/app/chroma_db videogames-chatbot
```

#### 2. "Redis connection failed"

**Solución:**
- Verifica que `REDIS_URL` esté configurado correctamente
- El sistema funciona sin Redis (fallback a memoria), pero con menor rendimiento
- En Railway: asegúrate de haber agregado el servicio de Redis

#### 3. "Rate limit exceeded" en Steam API

**Solución:**
- Steam limita a 100,000 requests/día
- El sistema tiene caché para mitigar esto
- Considera implementar un rate limiter en la API

#### 4. "Out of memory" en contenedor

**Solución:**
```bash
# Aumenta memoria en Railway
# Settings → Resources → Memory: 1GB → 2GB

# En AWS Fargate
# Modifica task definition: "memory": "2048"
```

#### 5. Health check failing

**Solución:**
```bash
# Verifica que el endpoint responda
curl http://localhost:8000/api/v1/health

# Revisa logs
railway logs  # Railway
aws logs tail /ecs/videogames-chatbot --follow  # AWS
```

### Monitoring y Logs

#### Railway

```bash
# Ver logs en tiempo real
railway logs

# Ver logs específicos
railway logs --service videogames-chatbot
```

#### AWS

```bash
# CloudWatch Logs
aws logs tail /ecs/videogames-chatbot --follow

# Métricas ECS
aws cloudwatch get-metric-statistics \
    --namespace AWS/ECS \
    --metric-name CPUUtilization \
    --dimensions Name=ServiceName,Value=videogames-chatbot-service \
    --start-time 2024-01-01T00:00:00Z \
    --end-time 2024-01-02T00:00:00Z \
    --period 3600 \
    --statistics Average
```

### Performance Tuning

#### 1. Optimizar caché

```python
# En .env
CACHE_TTL=7200  # 2 horas para datos de juegos
```

#### 2. Ajustar workers de Uvicorn

```bash
# En Dockerfile o comando de inicio
uvicorn src.main:app --workers 4 --host 0.0.0.0 --port 8000
```

#### 3. Configurar connection pooling

```python
# En steam_service.py ya está configurado httpx.AsyncClient
# Para múltiples workers, considera usar un pool compartido
```

---

## Migración Railway → AWS

Cuando necesites escalar:

1. **Exportar ChromaDB**
   ```bash
   # Backup de la base de datos vectorial
   tar -czf chroma_backup.tar.gz chroma_db/
   aws s3 cp chroma_backup.tar.gz s3://your-bucket/backups/
   ```

2. **Replicar variables de entorno**
   - Exporta variables de Railway
   - Impórtalas a AWS Secrets Manager

3. **Configurar dominio**
   - Apunta tu dominio al nuevo ALB de AWS
   - Configura SSL con ACM (AWS Certificate Manager)

4. **Testing**
   - Prueba exhaustivamente en staging
   - Usa Blue-Green deployment para cero downtime

---

## Soporte

Si tienes problemas:

1. Revisa los logs
2. Verifica variables de entorno
3. Consulta la documentación de Steam API y Anthropic
4. Abre un issue en GitHub

**¡Listo para desplegar!** 🚀
