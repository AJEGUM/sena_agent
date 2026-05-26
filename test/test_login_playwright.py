# test_login_playwright.py
from playwright.sync_api import sync_playwright
import time

def obtener_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("🌐 Abriendo portal...")
        page.goto("https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx")
        time.sleep(3)

        print("🖱️ Activando pestaña Aprendices...")
        # Buscar la pestaña por texto
        page.click("text=Aprendices")
        time.sleep(2)

        print("✍️ Llenando credenciales...")
        page.fill("#tbLoginUsuario", "1114000045")
        page.fill("#__tbPasswordUsuario", "aprendizsena")
        time.sleep(1)

        print("🔐 Haciendo login...")
        page.click("#ini_session_aprendiz")

        print("⏳ Esperando respuesta...")
        try:
            page.wait_for_url("**/Aprendices/Index**", timeout=15000)
            print("✅ Login exitoso")
        except:
            time.sleep(5)
            print(f"📄 URL actual: {page.url}")
            print(f"📄 Título: {page.title()}")

        cookies = page.context.cookies()
        browser.close()

        resultado = {}
        for c in cookies:
            resultado[c["name"]] = c["value"]

        print(f"🍪 Cookies obtenidas: {list(resultado.keys())}")
        return resultado

cookies = obtener_cookies()
print("\n✅ Listo:", cookies.get("ASP.NET_SessionId"))