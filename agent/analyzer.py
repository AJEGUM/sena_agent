import anthropic
from config.settings import ClaudeConfig


def construir_prompt(contenido_pagina):
    """
    Arma el prompt que le enviamos a Claude.
    Está separado para que sea fácil de modificar
    sin tocar la lógica principal.
    """
    return f"""Eres un asistente experto que ayuda a aprendices del SENA 
a encontrar la mejor empresa para realizar su práctica profesional.

Se te entrega el contenido extraído del portal de empresas del SENA,
ya filtrado por Valle del Cauca - Cali.

---
{contenido_pagina[:6000]}
---

Tu tarea es:

1. 📋 **Listar las últimas publicaciones encontradas** (máximo 5)
   - Nombre de la empresa
   - Sector o actividad
   - Qué perfil buscan o qué ofrecen
   - Fecha de publicación si aparece

2. ⭐ **Recomendar la mejor opción** explicando claramente por qué
   - Considera: reputación del sector, claridad de la oferta, perfil requerido

3. ⚠️ **Alertar** si no hay publicaciones recientes o si el contenido 
   no tiene información útil

Responde en español, de forma clara y amigable.
Usa emojis para que sea fácil de leer en Telegram.
Sé concreto, no uses frases largas innecesarias."""


def analizar_publicaciones(contenido_pagina):
    """
    Envía el contenido extraído a Claude y retorna
    el análisis y recomendación como texto.
    """
    print("🧠 Analizando publicaciones con Claude...")

    # Valida que haya contenido para analizar
    if not contenido_pagina or len(contenido_pagina.strip()) < 100:
        print("⚠️ Contenido muy corto o vacío para analizar")
        return "⚠️ No se encontró contenido suficiente para analizar. Puede que el portal haya cambiado o no haya publicaciones disponibles."

    client = anthropic.Anthropic(api_key=ClaudeConfig.API_KEY)

    try:
        mensaje = client.messages.create(
            model=ClaudeConfig.MODEL,
            max_tokens=ClaudeConfig.MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": construir_prompt(contenido_pagina)
                }
            ]
        )

        resultado = mensaje.content[0].text
        print("✅ Análisis completado")
        return resultado

    except anthropic.AuthenticationError:
        print("❌ API Key de Claude inválida")
        return "❌ Error de autenticación con Claude. Revisa tu API Key."

    except anthropic.RateLimitError:
        print("❌ Límite de requests alcanzado")
        return "❌ Límite de la API alcanzado. Intenta más tarde."

    except Exception as e:
        print(f"❌ Error inesperado en analyzer: {e}")
        return f"❌ Error al analizar: {str(e)}"