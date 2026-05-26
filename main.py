# main.py
import asyncio
import logging
import os
from datetime import datetime

from config.settings import validar_config
from agent.scraper import ejecutar_scraper
from agent.analyzer import analizar_publicaciones
from agent.notifier import enviar_reporte, enviar_alerta_error

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/agent.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

log = logging.getLogger(__name__)


async def correr_agente():
    log.info("=" * 50)
    log.info(f"🤖 Agente SENA iniciado — {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    log.info("=" * 50)

    try:
        validar_config()
    except ValueError as e:
        log.error(str(e))
        return

    # Sin await — ejecutar_scraper ya no es async
    contenido = await ejecutar_scraper()

    if not contenido:
        mensaje_error = "No se pudo extraer información del portal SENA"
        log.error(mensaje_error)
        enviar_alerta_error(mensaje_error)
        return

    analisis = analizar_publicaciones(contenido)
    enviado = enviar_reporte(analisis)

    if enviado:
        log.info("✅ Agente finalizado exitosamente")
    else:
        log.error("❌ El análisis se generó pero no se pudo enviar por Telegram")


if __name__ == "__main__":
    asyncio.run(correr_agente())