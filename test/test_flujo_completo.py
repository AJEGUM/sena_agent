# test_flujo_completo.py
import requests
from config.settings import SenaConfig

BASE = "https://caprendizaje.sena.edu.co"
cookies = {
    "cookiesession1": "",
    "ASP.NET_SessionId": "",
    "SGVACookie1": ""
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/sgva/APRENDICES/pag/AplicarAprendiz.aspx",
}

# ── 1. Obtener datos académicos del aprendiz ──
print("=== 1. ACADÉMICO ===")
r = requests.get(
    f"{BASE}/sgva/AprendizAcademico/AprendizConsultarAcademicos",
    cookies=cookies, headers=headers
)
print(f"Status: {r.status_code}")
data = r.json()
academicos = data.get("aaData", [])
print(f"Registros: {len(academicos)}")

# El JS usa el último registro: n[i-1]
ultimo = academicos[-1]
print(f"Último académico completo: {ultimo}")

# Según el JS:
# n[i-1][2]  → especialidadID (f)
# n[i-1][4]  → ciudad (e) — ojo: es el valor de ciudad, probablemente el id
# n[i-1][7]  → o (especialidad para el filtro)
# n[i-1][20] → academicoID (b)
especialidad_id = ultimo[7]   # o
ciudad_default  = ultimo[4]   # e  
academico_id    = ultimo[20]  # b

print(f"\n→ especialidadID (o): {especialidad_id}")
print(f"→ ciudad default (e): {ciudad_default}")
print(f"→ academicoID (b):    {academico_id}")

# ── 2. Obtener ciudades de Valle ──
print("\n=== 2. CIUDADES VALLE ===")
r2 = requests.get(
    f"{BASE}/sgva/Ciudad/CiudadByDptoId",
    params={"dpto": 76},
    cookies=cookies, headers=headers
)
ciudades = r2.json().get("aaData", [])
cali_id = next((c[0] for c in ciudades if "CALI" in c[1].upper()), "1")
print(f"Cali id: {cali_id}")

# ── 3. Buscar solicitudes con los parámetros correctos ──
print("\n=== 3. SOLICITUDES ===")
params = {
    "especialidad": especialidad_id,
    "dpto": 76,
    "ciudad": cali_id,
    "RSocial": "",
}
print(f"Params: {params}")
r3 = requests.get(
    f"{BASE}/sgva/Solicitudes/AprendizConsultarSolicitudesRequeridas",
    params=params,
    cookies=cookies, headers=headers
)
print(f"Status: {r3.status_code} — Tamaño: {len(r3.text)}")
print(f"Respuesta: {r3.text[:600]}")