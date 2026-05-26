import os
from dotenv import load_dotenv

# Lee el archivo .env y carga las variables
load_dotenv()


class SenaConfig:
    """Credenciales del portal SENA."""
    USER = os.getenv("SENA_USER")
    PASS = os.getenv("SENA_PASS")
    URL  = "https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx"

    # Filtros de búsqueda
    DEPARTAMENTO = "Valle del Cauca"
    CIUDAD       = "Cali"


class ClaudeConfig:
    """Configuración del modelo Claude."""
    API_KEY    = os.getenv("CLAUDE_API_KEY")
    MODEL      = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", 1000))


class TelegramConfig:
    """Credenciales del bot de Telegram."""
    TOKEN   = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def validar_config():
    """
    Revisa que todas las variables estén cargadas antes de correr el agente.
    Si falta alguna, avisa exactamente cuál es para que sea fácil de corregir.
    """
    requeridas = {
        "SENA_USER":       SenaConfig.USER,
        "SENA_PASS":       SenaConfig.PASS,
        "CLAUDE_API_KEY":  ClaudeConfig.API_KEY,
        "TELEGRAM_TOKEN":  TelegramConfig.TOKEN,
        "TELEGRAM_CHAT_ID": TelegramConfig.CHAT_ID,
    }

    faltantes = [nombre for nombre, valor in requeridas.items() if not valor]

    if faltantes:
        raise ValueError(
            f"❌ Faltan estas variables en el .env: {', '.join(faltantes)}"
        )

    print("✅ Configuración cargada correctamente")