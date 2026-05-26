import requests
from datetime import datetime
from config.settings import TelegramConfig


def enviar_mensaje(texto):
    """
    Envía un mensaje de texto al chat de Telegram configurado.
    Retorna True si fue exitoso, False si falló.
    """
    url = f"https://api.telegram.org/bot{TelegramConfig.TOKEN}/sendMessage"

    payload = {
        "chat_id": TelegramConfig.CHAT_ID,
        "text": texto,
        "parse_mode": "Markdown"  # Permite negritas, cursivas, etc.
    }

    try:
        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            print("✅ Mensaje enviado por Telegram")
            return True
        else:
            print(f"❌ Error Telegram {response.status_code}: {response.text}")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Sin conexión a internet")
        return False

    except requests.exceptions.Timeout:
        print("❌ Telegram tardó demasiado en responder")
        return False

    except Exception as e:
        print(f"❌ Error inesperado en notifier: {e}")
        return False


def enviar_reporte(analisis):
    """
    Arma el mensaje completo con encabezado y hora,
    y lo envía por Telegram.
    """
    hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    mensaje = (
        f"🎓 *Reporte SENA - Empresas en Cali*\n"
        f"🕐 Generado el {hora_actual}\n"
        f"{'─' * 30}\n\n"
        f"{analisis}"
    )

    return enviar_mensaje(mensaje)


def enviar_alerta_error(detalle_error):
    """
    Notifica cuando el agente falló para que sepas
    que algo salió mal sin tener que revisar logs manualmente.
    """
    hora_actual = datetime.now().strftime("%d/%m/%Y %H:%M")

    mensaje = (
        f"⚠️ *El agente SENA tuvo un problema*\n"
        f"🕐 {hora_actual}\n"
        f"{'─' * 30}\n\n"
        f"❌ {detalle_error}\n\n"
        f"Revisa los logs para más detalles."
    )

    return enviar_mensaje(mensaje)