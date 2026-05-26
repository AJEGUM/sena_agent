import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
from config.settings import SenaConfig


async def iniciar_sesion(page):
    print("🌐 Abriendo portal SENA...")
    await page.goto(SenaConfig.URL)
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(2)
    print("🔐 Iniciando sesión...")

    # Primero clic en la pestaña Aprendices para que sea visible
    await page.click("text=Aprendices")
    await asyncio.sleep(1)
    print("✅ Pestaña Aprendices activa")

    await page.fill("#tbLoginUsuario", SenaConfig.USER)
    print("✅ Usuario llenado")
    await page.fill("#__tbPasswordUsuario", SenaConfig.PASS)
    print("✅ Contraseña llenada")

    # Forzar clic aunque esté parcialmente oculto
    await page.click("#ini_session_aprendiz", force=True)
    print("✅ Botón clickeado")
    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(2)
    print("✅ Sesión iniciada")
    return True


async def aplicar_filtros(page):
    """
    Navega a 'Buscar Empresa' y aplica los filtros
    de departamento y ciudad definidos en settings.
    """
    print("🔍 Navegando a Buscar Empresa...")
    try:
        # Busca el enlace por texto visible en el menú
        await page.click("text=Buscar empresa", timeout=5000)
    except PlaywrightTimeout:
        try:
            await page.click("text=Empresa", timeout=5000)
        except PlaywrightTimeout:
            print("❌ No se encontró el menú 'Buscar Empresa'")
            return False

    await page.wait_for_load_state("networkidle")
    await asyncio.sleep(2)

    print(f"🗺️ Aplicando filtros: {SenaConfig.DEPARTAMENTO} / {SenaConfig.CIUDAD}...")
    try:
        # Selector de departamento
        await page.select_option(
            "select[id*='departamento'], select[name*='departamento'], select[id*='Departamento']",
            label=SenaConfig.DEPARTAMENTO
        )
        await asyncio.sleep(1)

        # Selector de ciudad (se carga después del departamento)
        await page.select_option(
            "select[id*='ciudad'], select[name*='ciudad'], select[id*='municipio']",
            label=SenaConfig.CIUDAD
        )
        await asyncio.sleep(1)

        # Botón buscar
        await page.click("input[value*='Buscar'], button:has-text('Buscar')")
        await page.wait_for_load_state("networkidle")
        await asyncio.sleep(3)

        print("✅ Filtros aplicados")
        return True

    except PlaywrightTimeout:
        print("❌ Error aplicando filtros — puede que los selectores hayan cambiado")
        return False


async def extraer_publicaciones(page):
    """
    Extrae el texto visible de los resultados.
    Retorna el contenido como string para enviarlo a Claude.
    """
    print("📋 Extrayendo publicaciones...")

    # Intenta obtener solo la tabla de resultados
    # Si no existe ese selector, toma todo el body
    try:
        contenido = await page.inner_text(
            "table, div[id*='resultado'], div[id*='grid'], div[class*='resultado']",
            timeout=3000
        )
    except PlaywrightTimeout:
        contenido = await page.inner_text("body")

    print(f"✅ Extraídos {len(contenido)} caracteres")
    return contenido


async def ejecutar_scraper():
    """
    Función principal que orquesta todo el flujo:
    login → filtros → extracción.
    Retorna el contenido extraído o None si algo falló.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            login_ok = await iniciar_sesion(page)
            if not login_ok:
                return None

            filtros_ok = await aplicar_filtros(page)
            if not filtros_ok:
                return None

            contenido = await extraer_publicaciones(page)
            return contenido

        except Exception as e:
            print(f"❌ Error inesperado en scraper: {e}")
            return None

        finally:
            # Siempre cierra el navegador, haya error o no
            await browser.close()
            print("🔒 Navegador cerrado")