# 💬 Example Queries

A collection of example queries you can try with the Videogames Chatbot.

## 🎯 General Information

### What can you do?
```json
{
  "message": "¿Qué tipo de información puedes darme sobre videojuegos?",
  "use_tools": false
}
```

### Capabilities
```json
{
  "message": "Explícame cómo puedes ayudarme a encontrar videojuegos",
  "use_tools": false
}
```

---

## 🔍 Search & Discovery

### Simple Search
```json
{
  "message": "Busca el juego Elden Ring",
  "use_tools": true
}
```

### Genre-based Search
```json
{
  "message": "Busca juegos de estrategia lanzados en 2024",
  "use_tools": true
}
```

### Developer Search
```json
{
  "message": "¿Qué juegos ha desarrollado FromSoftware?",
  "use_tools": true
}
```

---

## 📊 Game Analysis

### User Satisfaction
```json
{
  "message": "¿Qué tan satisfechos están los jugadores con Baldur's Gate 3?",
  "use_tools": true
}
```

### Difficulty Analysis
```json
{
  "message": "¿Qué tan difícil es Dark Souls 3 según las reseñas?",
  "use_tools": true
}
```

### Originality & Innovation
```json
{
  "message": "Analiza la originalidad de Hades según las opiniones de los jugadores",
  "use_tools": true
}
```

### Artistic Quality
```json
{
  "message": "¿Qué opinan los jugadores sobre el apartado artístico de Hollow Knight?",
  "use_tools": true
}
```

---

## 🎮 Recommendations

### Similar Games
```json
{
  "message": "Recomiéndame juegos similares a The Witcher 3",
  "use_tools": true
}
```

### Based on Preferences
```json
{
  "message": "Quiero juegos de rol con buena historia y combate desafiante",
  "use_tools": true
}
```

### Difficulty-based
```json
{
  "message": "Recomiéndame juegos tipo Dark Souls pero más accesibles para principiantes",
  "use_tools": true
}
```

### Platform-specific
```json
{
  "message": "¿Qué buenos juegos indie están disponibles para PC?",
  "use_tools": true
}
```

---

## 📈 Reviews & Opinions

### General Opinion
```json
{
  "message": "¿Qué opinan los jugadores sobre Cyberpunk 2077 actualmente?",
  "use_tools": true
}
```

### Pros and Cons
```json
{
  "message": "Dime los aspectos más valorados y más criticados de Starfield",
  "use_tools": true
}
```

### Comparison
```json
{
  "message": "Compara las opiniones de los jugadores sobre Elden Ring vs Dark Souls 3",
  "use_tools": true
}
```

---

## ⏰ Game Information

### Release Date
```json
{
  "message": "¿Cuándo salió Baldur's Gate 3?",
  "use_tools": true
}
```

### Price Information
```json
{
  "message": "¿Cuánto cuesta Hogwarts Legacy?",
  "use_tools": true
}
```

### Playtime
```json
{
  "message": "¿Cuántas horas de juego tiene en promedio Persona 5 Royal?",
  "use_tools": true
}
```

### Current Players
```json
{
  "message": "¿Cuánta gente está jugando Counter-Strike 2 ahora mismo?",
  "use_tools": true
}
```

---

## 🏆 Exclusives & Special Features

### Exclusivity
```json
{
  "message": "¿God of War es exclusivo de alguna plataforma?",
  "use_tools": true
}
```

### Special Features
```json
{
  "message": "¿Qué características especiales tiene el multijugador de Elden Ring?",
  "use_tools": true
}
```

---

## 💎 Detailed Analysis Requests

### Comprehensive Analysis
```json
{
  "message": "Dame un análisis completo de Hades incluyendo satisfacción, dificultad, originalidad y apartado artístico",
  "use_tools": true
}
```

### Target Audience
```json
{
  "message": "¿Para qué tipo de jugador está recomendado Sekiro: Shadows Die Twice?",
  "use_tools": true
}
```

### Game Length
```json
{
  "message": "¿Cuánto dura aproximadamente completar The Legend of Zelda: Tears of the Kingdom?",
  "use_tools": true
}
```

---

## 🔄 Conversational Examples

### Multi-turn Conversation

**Turn 1:**
```json
{
  "message": "Busca Hollow Knight",
  "use_tools": true
}
```

**Turn 2:**
```json
{
  "message": "¿Qué opinan los jugadores sobre su dificultad?",
  "conversation_history": [
    {"role": "user", "content": "Busca Hollow Knight"},
    {"role": "assistant", "content": "[Previous response]"}
  ],
  "use_tools": true
}
```

**Turn 3:**
```json
{
  "message": "Recomiéndame juegos similares pero más fáciles",
  "conversation_history": [
    {"role": "user", "content": "Busca Hollow Knight"},
    {"role": "assistant", "content": "[Response 1]"},
    {"role": "user", "content": "¿Qué opinan los jugadores sobre su dificultad?"},
    {"role": "assistant", "content": "[Response 2]"}
  ],
  "use_tools": true
}
```

---

## 🎲 Creative Queries

### Best of Genre
```json
{
  "message": "¿Cuáles son los mejores juegos de plataformas 2D según las reseñas?",
  "use_tools": true
}
```

### Hidden Gems
```json
{
  "message": "Recomiéndame juegos indie poco conocidos pero muy bien valorados",
  "use_tools": true
}
```

### Trending Games
```json
{
  "message": "¿Cuáles son los juegos más populares en Steam ahora mismo?",
  "use_tools": true
}
```

### Worth It?
```json
{
  "message": "¿Vale la pena comprar Red Dead Redemption 2 en 2024?",
  "use_tools": true
}
```

---

## 🌟 Advanced Queries

### Sentiment Trends
```json
{
  "message": "¿Cómo ha cambiado la opinión de los jugadores sobre No Man's Sky desde su lanzamiento?",
  "use_tools": true
}
```

### Community Reception
```json
{
  "message": "Analiza cómo fue recibido Starfield por la comunidad",
  "use_tools": true
}
```

### Meta-scores vs User Reviews
```json
{
  "message": "Compara la puntuación de Metacritic con las reseñas de usuarios de The Last of Us Part II",
  "use_tools": true
}
```

---

## Tips for Better Results

1. **Be Specific**: The more specific your query, the better the response
   - ❌ "Dime sobre este juego"
   - ✅ "Analiza la dificultad y duración de Sekiro"

2. **Use Context**: Reference previous messages for better conversation flow
   - Use `conversation_history` parameter

3. **Enable Tools**: Set `use_tools: true` for data-driven responses
   - Simple questions → `use_tools: false`
   - Data queries → `use_tools: true`

4. **Ask Follow-ups**: The bot remembers context
   - "¿Y qué hay de su banda sonora?"
   - "Compáralo con el anterior"

---

## Testing These Examples

### Using cURL:

```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Busca Elden Ring y dime qué opinan los jugadores",
    "use_tools": true
  }'
```

### Using Python:

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/chat",
        json={
            "message": "Busca Elden Ring y dime qué opinan los jugadores",
            "use_tools": True
        }
    )
    print(response.json()["response"])
```

### Using the Interactive Docs:

Visit http://localhost:8000/docs and try the queries directly!

---

**Have more interesting queries? Contribute them back to the project!** 🎮
