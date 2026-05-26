# agent/cookie_manager.py
from playwright.async_api import async_playwright
import asyncio
import random

async def obtener_cookies_frescas(user: str, password: str) -> dict:
    print("Renovando cookies via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--window-size=1280,720",
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-CO",
            timezone_id="America/Bogota",
        )

        # Ocultar que es un browser automatizado
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            window.chrome = { runtime: {} };
        """)

        page = await context.new_page()

        print("Cargando pagina de login...")
        await page.goto(
            "https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx",
            wait_until="domcontentloaded",
            timeout=30000
        )
        await asyncio.sleep(random.uniform(2, 4))

        print("Activando pestana Aprendices...")
        await page.click("text=Aprendices")
        await asyncio.sleep(random.uniform(1, 2))

        # Esperar que el formulario sea visible
        await page.wait_for_selector("#tbLoginUsuario", state="visible", timeout=10000)

        # Escribir como humano — letra por letra con delay
        print("Escribiendo credenciales...")
        await page.click("#tbLoginUsuario")
        for char in user:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))

        await asyncio.sleep(random.uniform(0.3, 0.7))

        await page.click("#__tbPasswordUsuario")
        for char in password:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))

        await asyncio.sleep(random.uniform(0.5, 1))

        print("Haciendo login...")
        await page.click("#ini_session_aprendiz")

        # Esperar redirección
        try:
            await page.wait_for_url("**Aprendices**", timeout=20000)
            print(f"Login exitoso - URL: {page.url}")
        except Exception as e:
            print(f"URL actual tras login: {page.url}")

        await asyncio.sleep(2)
        cookies = await context.cookies()
        await browser.close()

    resultado = {}
    for c in cookies:
        resultado[c["name"]] = c["value"]

    print(f"Cookies obtenidas: {list(resultado.keys())}")
    return resultado