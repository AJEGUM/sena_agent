# test_bundle.py
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
}

# Descargar el bundle JS de la página de buscar empresa
r = requests.get(
    f"{BASE}/sgva/bundles/aprendiz_solicitudes",
    cookies=cookies,
    headers=headers,
)
print(f"Status: {r.status_code} — Tamaño: {len(r.text)}")

# Buscar la función que llama a AprendizConsultarSolicitudesRequeridas
js = r.text
idx = js.find("AprendizConsultarSolicitudesRequeridas")
if idx != -1:
    print("\n=== CONTEXTO ALREDEDOR DEL ENDPOINT ===")
    print(js[max(0, idx-500):idx+500])
else:
    print("❌ No se encontró el endpoint en el bundle")
    # Guardar para inspección manual
    with open("bundle.js", "w", encoding="utf-8") as f:
        f.write(js)
    print("💾 Bundle guardado en bundle.js")