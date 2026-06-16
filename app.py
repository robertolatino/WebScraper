import streamlit as st
import io
import os
os.system("playwright install chromium firefox")
from docx import Document

# Importar configuración centralizada
try:
    from config import STREAMLIT_CONFIG, obtener_url_base
except ImportError:
    # Valores por defecto si no está disponible el archivo config
    STREAMLIT_CONFIG = {
        "page_title": "Testing Automation Suite",
        "page_icon": "",
        "layout": "centered"
    }
    def obtener_url_base(plataforma):
        if plataforma == "Edelvives Digital Plus (EPD)":
            return "https://publisher.edelvivesdigitalplus.com/"
        return "https://publisher.bymedigital.com/"

# --- PREPARACIÓN DE LAS CONEXIONES FUTURAS ---
try:
    from recolector import ejecutar_recoleccion
    from scraper import ejecutar_extraccion_enunciados, agregar_html_a_docx
except ImportError:
    # Esto evitará que la web falle antes de que modifiquemos los otros archivos
    def ejecutar_recoleccion(*args, **kwargs): return []
    def ejecutar_extraccion_enunciados(*args, **kwargs): return []
    def agregar_html_a_docx(*args, **kwargs): pass

# --- CONFIGURACIÓN DE LA UI ---
st.set_page_config(
    page_title=STREAMLIT_CONFIG.get("page_title", "Testing Automation Suite"),
    page_icon=STREAMLIT_CONFIG.get("page_icon", ""),
    layout=STREAMLIT_CONFIG.get("layout", "centered")
)

st.title("Testing Automation Suite")
st.write("Recolección y extracción automatizada de contenidos.")
st.markdown("---")

# =========================================================================
# 1. SELECCIÓN DE PUBLISHER & 2. CREDENCIALES 
# =========================================================================
st.sidebar.header("⚙️ Configuración del Entorno")

# Paso 1: Selección del Publisher
plataforma = st.sidebar.selectbox(
    "1. ¿Qué plataforma quieres usar?",
    ["Edelvives Digital Plus (EPD)", "ByME Digital / Got It"]
)

# Asignación dinámica de la URL desde config
url_base = obtener_url_base(plataforma)

st.sidebar.markdown("---")

# Paso 2: Credenciales de acceso
st.sidebar.header("Credenciales de Acceso")
usuario = st.sidebar.text_input("Usuario / Correo", placeholder="ejemplo@edelvives.es")
contrasena = st.sidebar.text_input("Contraseña", type="password")

# Cuadro informativo para confirmar la conexión activa
st.sidebar.info(f"Conectando a:\n`{url_base}`")


# =========================================================================
# PESTAÑAS DE TRABAJO
# =========================================================================
tab_recolector, tab_extractor = st.tabs(["1. Recolector de Códigos", "Docx 2. Extractor de Enunciados"])

# --- PESTAÑA 1: RECOLECTOR ---
with tab_recolector:
    st.header("Herramienta de Recolección")
    st.write("Busca de forma masiva todos los códigos de tipo 'Question' asociados a un libro.")
    
    # Paso 3: Código padre del libro
    codigo_libro = st.text_input("3. Introduce el código del libro:", placeholder="Ej: 225253_MAT1")
    
    if st.button("Iniciar módulo 'recolector.py'", key="btn_rec"):
        if not usuario or not contrasena or not codigo_libro:
            st.error("Error: Asegúrate de rellenar las credenciales en la barra lateral y el código del libro.")
        else:
            progreso = st.status("Llamando a 'recolector.py'...")
            try:
                # Pasamos las variables dinámicas recopiladas en la UI
                lista_final = ejecutar_recoleccion(url_base, usuario, contrasena, codigo_libro, progreso)
                
                progreso.update(label="¡Proceso finalizado por el recolector!", state="complete")
                st.success(f"Se han encontrado {len(lista_final)} códigos válidos.")
                
                # Generador del botón de descarga para el .txt
                txt_data = "\n".join(lista_final)
                st.download_button(
                    label="Descargar lista de códigos (.txt)",
                    data=txt_data,
                    file_name=f"codigos_{codigo_libro}.txt",
                    mime="text/plain"
                )
            except Exception as e:
                progreso.update(label="El módulo falló de forma inesperada.", state="error")
                st.error(f"Detalle del fallo: {e}")

# --- PESTAÑA 2: EXTRACTOR ---
with tab_extractor:
    st.header("Herramienta de Extracción")
    st.write("Procesa un archivo de códigos para extraer sus enunciados maquetados en un Word.")
    
    # En este módulo el usuario sube el archivo generado previamente
    archivo_subido = st.file_uploader("Sube tu archivo de códigos (.txt):", type=["txt"])
    
    if st.button("Iniciar módulo 'scraper.py'", key="btn_ext"):
        if not usuario or not contrasena or not archivo_subido:
            st.error("Error: Asegúrate de rellenar las credenciales y subir un archivo .txt válido.")
        else:
            # Procesamos el archivo subido en memoria
            contenido_txt = archivo_subido.read().decode("utf-8")
            lista_codigos = [linea.strip() for linea in contenido_txt.splitlines() if linea.strip()]
            
            st.info(f"Cargados {len(lista_codigos)} códigos para procesar en {plataforma}.")
            progreso = st.status("Llamando a 'scraper.py'...")
            
            try:
                # Pasamos las variables dinámicas recopiladas en la UI
                resultados = ejecutar_extraccion_enunciados(url_base, usuario, contrasena, lista_codigos, progreso)
                
                progreso.update(label="¡Extracción completada!", state="complete")
                
                # Maquetación del Word final
                doc = Document()
                doc.add_heading(f'Enunciados Extraídos - {plataforma}', 0)
                for cod, desc_html in resultados:
                    agregar_html_a_docx(desc_html, doc, cod)
                
                # Guardamos en un buffer en memoria para la descarga web inmediata
                docx_buffer = io.BytesIO()
                doc.save(docx_buffer)
                docx_buffer.seek(0)
                
                st.success("Documento Word generado listo para descarga.")
                st.download_button(
                    label="Descargar Documento (.docx)",
                    data=docx_buffer,
                    file_name=f"enunciados_{plataforma.split()[0]}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
            except Exception as e:
                progreso.update(label="El módulo falló de forma inesperada.", state="error")
                st.error(f"Detalle del fallo: {e}")