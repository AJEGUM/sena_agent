# test_solicitudes.py
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

# Probar variantes del endpoint de solicitudes
variantes = [
    {"idDepartamento": 76, "idCiudad": 1, "razonSocial": ""},
    {"departamento": 76, "ciudad": 1, "razonSocial": ""},
    {"dpto": 76, "ciudad": 1, "razonSocial": ""},
    {"dpto": 76, "idCiudad": 1, "razonSocial": ""},
    {"idDepartamento": 76, "ciudad": 1, "razonSocial": ""},
]

for params in variantes:
    r = requests.get(
        f"{BASE}/sgva/Solicitudes/AprendizConsultarSolicitudesRequeridas",
        params=params, cookies=cookies, headers=headers
    )
    print(f"params={params} → status={r.status_code} tamaño={len(r.text)}")
    if r.status_code == 200:
        print(f"  ✅ RESPUESTA: {r.text[:400]}")
        break