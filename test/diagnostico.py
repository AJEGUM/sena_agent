import asyncio
from playwright.async_api import async_playwright

async def diagnosticar_post_login():
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        page = await browser.new_page()

        # Simular navegador real
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720},
            locale="es-CO",
        )

        page = await context.new_page()

        # Ocultar que es Playwright
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print("🔐 Haciendo login...")
        await page.goto("https://caprendizaje.sena.edu.co/sgva/SGVA_Diseno/pag/login.aspx", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)
        await page.click("text=Aprendices")
        await asyncio.sleep(1)
        await page.fill("#tbLoginUsuario", "1114000045")
        await page.fill("#__tbPasswordUsuario", "aprendizsena")
        await page.click("#ini_session_aprendiz", force=True)

        print("⏳ Esperando redirección...")
        try:
            await page.wait_for_url("**/Aprendices/**", timeout=40000)
            print(f"✅ Login exitoso — URL: {page.url}")
        except:
            print(f"⚠️ URL actual: {page.url}")

        await asyncio.sleep(8)
        await page.screenshot(path="post_login.png", full_page=True)
        print("📸 Captura guardada")

        frames = page.frames
        print(f"\n🔍 Frames: {len(frames)}")
        for f in frames:
            print(f"  {f.url}")

        await asyncio.sleep(10)
        await browser.close()

asyncio.run(diagnosticar_post_login())