# agent/cookie_manager.py
from playwright.async_api import async_playwright
import asyncio

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
            ]
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
        )
        page = await context.new_page()

        # Ocultar que es Playwright
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        await page.goto("https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        await page.click("text=Aprendices")
        await page.wait_for_selector("#ini_session_aprendiz", state="visible", timeout=15000)
        await asyncio.sleep(2)

        await page.fill("#tbLoginUsuario", user)
        await page.fill("#__tbPasswordUsuario", password)
        await asyncio.sleep(1)

        await page.click("#ini_session_aprendiz", force=True)
        
        # Esperar la URL de destino en vez de networkidle
        try:
            await page.wait_for_url("**/Aprendices/Index**", timeout=20000)
        except:
            await asyncio.sleep(8)
            print(f"URL actual: {page.url}")

        cookies = await context.cookies()
        await browser.close()

    resultado = {}
    for c in cookies:
        resultado[c["name"]] = c["value"]

    print(f"Cookies obtenidas: {list(resultado.keys())}")
    return resultado