# config/settings.py
import os
from dotenv import load_dotenv

load_dotenv()

class SenaConfig:
    USER            = os.getenv("SENA_USER")
    PASS            = os.getenv("SENA_PASS")
    COOKIE_SESSION1 = os.getenv("SENA_COOKIE_SESSION1")
    ASPNET_SESSION  = os.getenv("SENA_ASPNET_SESSION")
    SGVA_COOKIE1    = os.getenv("SENA_SGVA_COOKIE1")
    DEPARTAMENTO    = "VALLE"
    CIUDAD          = "CALI"


class ClaudeConfig:
    API_KEY    = os.getenv("CLAUDE_API_KEY")
    MODEL      = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", 4096))


class TelegramConfig:
    TOKEN   = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def validar_config():
    errores = []
    if not SenaConfig.USER:
        errores.append("Falta SENA_USER en .env")
    if not SenaConfig.PASS:
        errores.append("Falta SENA_PASS en .env")
    if not ClaudeConfig.API_KEY:
        errores.append("Falta CLAUDE_API_KEY en .env")
    if not TelegramConfig.TOKEN:
        errores.append("Falta TELEGRAM_TOKEN en .env")
    if not TelegramConfig.CHAT_ID:
        errores.append("Falta TELEGRAM_CHAT_ID en .env")
    if errores:
        raise ValueError("❌ Configuración incompleta:\n" + "\n".join(f"  - {e}" for e in errores))