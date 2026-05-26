# agent/cookie_manager.py
from playwright.async_api import async_playwright
import asyncio

async def obtener_cookies_frescas(user: str, password: str) -> dict:
    print("🔐 Renovando cookies via Playwright...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx")
        await asyncio.sleep(3)

        await page.click("text=Aprendices")
        await asyncio.sleep(2)

        await page.fill("#tbLoginUsuario", user)
        await page.fill("#__tbPasswordUsuario", password)
        await asyncio.sleep(1)

        await page.click("#ini_session_aprendiz")
        await asyncio.sleep(5)

        cookies = await page.context.cookies()
        await browser.close()

    resultado = {}
    for c in cookies:
        resultado[c["name"]] = c["value"]

    print(f"✅ Cookies renovadas: {list(resultado.keys())}")
    return resultado