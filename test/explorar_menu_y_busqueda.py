# explorar_menu_y_busqueda.py
import requests
import json
from bs4 import BeautifulSoup

BASE = "https://caprendizaje.sena.edu.co"

cookies = {
    "cookiesession1": "",
    "ASP.NET_SessionId": "",
    "SGVACookie1": ""
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json, text/javascript, */*",
    "Accept-Language": "es-419,es;q=0.7",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": f"{BASE}/sgva/Aprendices/Index",
}

# ── 1. Llamar al endpoint del menú para obtener la URL real de Buscar Empresa ──
print("=== 1. MENU AJAX ===")
r = requests.get(f"{BASE}/sgva/MenuAprendiz/MenuAprendiz", cookies=cookies, headers=headers)
print(f"Status: {r.status_code}")
try:
    data = r.json()
    items = data.get("aaData", [])
    for i, item in enumerate(items):
        print(f"  [{i}] → {item}")
except Exception as e:
    print(f"No es JSON: {e}")
    print(r.text[:500])

# ── 2. Intentar la URL del menú viejo (hardcodeada en el HTML) ──
print("\n=== 2. PÁGINA BUSCAR EMPRESA (vieja) ===")
r2 = requests.get(f"{BASE}/sgva/APRENDICES/pag/AplicarAprendiz.aspx", cookies=cookies, headers={**headers, "Accept": "text/html"})
print(f"Status: {r2.status_code} — URL final: {r2.url} — Tamaño: {len(r2.text)}")
with open("buscar_empresa.html", "w", encoding="utf-8") as f:
    f.write(r2.text)
print("💾 Guardado en buscar_empresa.html")

# Buscar forms y selects
soup = BeautifulSoup(r2.text, "html.parser")
print("\nFORMS encontrados:")
for form in soup.find_all("form"):
    print(f"  action={form.get('action')} method={form.get('method')}")

print("\nSELECTS encontrados:")
for sel in soup.find_all("select"):
    print(f"  name={sel.get('name')} id={sel.get('id')}")
    opts = sel.find_all("option")[:5]
    for o in opts:
        print(f"    val='{o.get('value')}' → {o.get_text(strip=True)}")

# ── 3. Intentar también la URL nueva del menú si existe ──
print("\n=== 3. ENDPOINT BUSCAR EMPRESA (nuevo MVC) ===")
urls_a_probar = [
    "/sgva/Aprendices/BuscarEmpresa",
    "/sgva/Empresa/BuscarEmpresa",
    "/sgva/AprendizEmpresa/BuscarEmpresa",
    "/sgva/Aprendices/Empresa",
]
for url in urls_a_probar:
    r3 = requests.get(f"{BASE}{url}", cookies=cookies, headers={**headers, "Accept": "text/html"}, allow_redirects=True)
    print(f"  {url} → {r3.status_code} ({len(r3.text)} chars) final={r3.url}")