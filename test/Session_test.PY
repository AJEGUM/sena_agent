import requests

# Cookies de tu sesión activa de Brave
cookies = {
    "cookiesession1": "",
    "ASP.NET_SessionId": "",
    "SGVACookie1": ""
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "es-419,es;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

print("🌐 Probando acceso con sesión activa...")
response = requests.get(
    "https://caprendizaje.sena.edu.co/sgva/Aprendices/Index",
    cookies=cookies,
    headers=headers,
    timeout=30
)

print(f"📡 Status: {response.status_code}")
print(f"📍 URL final: {response.url}")
print(f"📄 Tamaño respuesta: {len(response.text)} caracteres")

# Guardar HTML para inspeccionarlo
with open("respuesta.html", "w", encoding="utf-8") as f:
    f.write(response.text)
print("💾 HTML guardado en respuesta.html")

# Verificar si estamos logueados
if "Cerrar" in response.text or "sesión" in response.text.lower() or "aprendiz" in response.text.lower():
    print("✅ Sesión válida — estamos dentro del portal")
else:
    print("⚠️ Puede que la sesión haya expirado")