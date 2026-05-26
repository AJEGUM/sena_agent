# test_ciudades.py
import requests

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

# Probar variantes del parámetro
variantes = [
    {"id": 76},
    {"idDepartamento": 76},
    {"departamentoId": 76},
    {"IdDepartamento": 76},
    {"dpto": 76},
]

for params in variantes:
    r = requests.get(f"{BASE}/sgva/Ciudad/CiudadByDptoId", params=params, cookies=cookies, headers=headers)
    print(f"params={params} → status={r.status_code} tamaño={len(r.text)}")
    if r.status_code == 200:
        print(f"  ✅ RESPUESTA: {r.text[:300]}")
        break