"""
Configuración centralizada del proyecto WebScraper
Carga variables de entorno de forma segura
"""

import os
from pathlib import Path

# Cargar variables de entorno desde .env si existe
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # Si python-dotenv no está instalado, usar variables del sistema
    pass

# Configuración de plataformas
PLATAFORMAS = {
    "Edelvives Digital Plus (EPD)": {
        "url": os.getenv("URL_EPD", "https://publisher.edelvivesdigitalplus.com/"),
        "navegador": "chromium"
    },
    "ByME Digital / Got It": {
        "url": os.getenv("URL_BYME", "https://publisher.bymedigital.com/"),
        "navegador": "firefox"
    }
}

# Configuración de Playwright
PLAYWRIGHT_CONFIG = {
    "headless": True,  # Siempre True para aplicaciones web
    "timeout": 30000,  # 30 segundos
}

# Configuración de Streamlit (opcional)
STREAMLIT_CONFIG = {
    "page_title": "Testing Automation Suite",
    "page_icon": "🤖",
    "layout": "centered"
}

def obtener_url_base(plataforma_nombre):
    """Obtiene la URL base de una plataforma por su nombre."""
    if plataforma_nombre in PLATAFORMAS:
        return PLATAFORMAS[plataforma_nombre]["url"]
    return PLATAFORMAS["Edelvives Digital Plus (EPD)"]["url"]

def obtener_navegador(plataforma_nombre):
    """Obtiene el navegador a usar para una plataforma."""
    if plataforma_nombre in PLATAFORMAS:
        return PLATAFORMAS[plataforma_nombre]["navegador"]
    return "chromium"
