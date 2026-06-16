import time
from playwright.sync_api import sync_playwright

def ejecutar_recoleccion(url_base, usuario, contrasena, codigo_libro, progreso_st):
    with sync_playwright() as p:
        # headless=True 
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def aplicar_filtro_global():
            try:
                progreso_st.update(label="Aplicando filtro de 'Question'...", state="running")
                page.locator('.input-search-filter__button').first.click()
                page.wait_for_timeout(1000)
                page.locator('[id="Tipo de contenido"]').first.click()
                page.wait_for_timeout(1000)
                
                # Verificamos si la casilla ya está marcada antes de hacer clic para no desmarcarla
                checkbox = page.locator('label:has-text("Question") input[type="checkbox"]').first
                if not checkbox.is_checked():
                    page.locator('label:has-text("Question")').first.click()
                    page.wait_for_timeout(500)
                
                page.locator('button[aria-label="Aplicar filtros"]').first.click()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2000)
            except Exception as e:
                pass

        # --- NAVEGACIÓN Y LOGIN ---
        progreso_st.update(label="Accediendo a la plataforma...", state="running")
        page.goto(url_base + "/auth/login")
        
        page.get_by_placeholder("Nombre de usuario").fill(usuario)
        page.get_by_placeholder("Contraseña").fill(contrasena)
        page.get_by_role("button", name="Iniciar sesión").click()
        page.wait_for_load_state("networkidle")
        
        progreso_st.update(label="Navegando a la sección de Contenidos...", state="running")
        page.locator('div[aria-label="Contenidos"]').first.click()
        page.wait_for_timeout(1000)
        
        page.locator('.wrapper-list-menu__item a[href="/contents"]').first.click()
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        
        # 1. BUSCAMOS EL LIBRO
        progreso_st.update(label=f"Buscando el libro: {codigo_libro}...", state="running")
        buscador = page.locator('input[data-testid="search"]')
        buscador.fill("") 
        buscador.fill(codigo_libro)
        buscador.press("Enter")
        
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # 2. FILTRO
        aplicar_filtro_global()

        codigos_recolectados = set() 
        pagina_actual = 1
        
        # --- BUCLE DE RECOLECCIÓN ---
        while True:
            progreso_st.update(label=f"Analizando y recolectando códigos de la página {pagina_actual}...", state="running")
            
            elementos = page.locator('tr:has(td:has-text("Question")) .table-body-cell-edit a').all()
            
            if not elementos:
                # Si no hay elementos en la página actual, hemos terminado
                break
                
            for el in elementos:
                codigo = el.inner_text().strip()
                if codigo:
                    codigos_recolectados.add(codigo)
            
            btn_siguiente = page.locator('button[aria-label="Go to next page"], button[aria-label="Ir a la página siguiente"], ul.MuiPagination-ul li:last-child button').first
            
            if not btn_siguiente.is_visible() or btn_siguiente.is_disabled():
                break
                
            btn_siguiente.click()
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(2000) 
            
            pagina_actual += 1

        browser.close()
        
        # Devolvemos la lista ordenada a app.py
        return sorted(list(codigos_recolectados))