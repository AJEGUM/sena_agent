import requests
from config.settings import SenaConfig
from agent.cookie_manager import obtener_cookies_frescas

BASE = "https://caprendizaje.sena.edu.co"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/sgva/APRENDICES/pag/AplicarAprendiz.aspx",
}

async def ejecutar_scraper():
    print("🤖 Iniciando scraper...")

    cookies = await obtener_cookies_frescas(SenaConfig.USER, SenaConfig.PASS)

    session = requests.Session()
    session.cookies.update(cookies)
    session.headers.update(HEADERS)

    print("📚 Obteniendo perfil académico...")
    r = session.get(f"{BASE}/sgva/AprendizAcademico/AprendizConsultarAcademicos", timeout=15)

    if "text/html" in r.headers.get("Content-Type", ""):
        print("❌ Login fallido")
        return None

    r.raise_for_status()
    academicos = r.json().get("aaData", [])

    if not academicos:
        print("❌ Sin datos académicos")
        return None

    ultimo = academicos[-1]
    if ultimo[16] != "1":
        print(f"⚠️ Estado no disponible: {ultimo[17]}")
        return None

    especialidad_id = ultimo[7]
    print(f"✅ Especialidad: {ultimo[8]} (id={especialidad_id})")

    print("🏙️ Obteniendo ciudades de Valle...")
    r2 = session.get(f"{BASE}/sgva/Ciudad/CiudadByDptoId", params={"dpto": 76}, timeout=15)
    r2.raise_for_status()
    ciudades = r2.json().get("aaData", [])
    cali_id = next((c[0] for c in ciudades if "CALI" in c[1].upper()), "1")
    print(f"✅ Cali id: {cali_id}")

    print("🔍 Buscando solicitudes en Cali...")
    r3 = session.get(
        f"{BASE}/sgva/Solicitudes/AprendizConsultarSolicitudesRequeridas",
        params={"especialidad": especialidad_id, "dpto": 76, "ciudad": cali_id, "RSocial": ""},
        timeout=20,
    )
    r3.raise_for_status()
    solicitudes = r3.json().get("aaData", [])

    if not solicitudes:
        return "⚠️ No hay solicitudes disponibles en Cali para tu perfil."

    print(f"✅ {len(solicitudes)} solicitudes encontradas")

    lineas = [f"Solicitudes de práctica en Cali, Valle: {len(solicitudes)}\n"]
    for i, s in enumerate(solicitudes, 1):
        lineas.append(f"--- Empresa {i} ---")
        lineas.append(f"  Empresa:        {s[1].strip()}")
        lineas.append(f"  Ciudad:         {s[3].strip()}")
        lineas.append(f"  Aprendices req: {s[4]}")
        lineas.append(f"  Fecha creación: {s[5]}")
        lineas.append(f"  Fecha cierre:   {s[6]}")
        lineas.append("")

    return "\n".join(lineas)