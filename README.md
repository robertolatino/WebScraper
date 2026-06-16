# WebScraper
Herramienta RPA con Python, Streamlit y Playwright para automatizar la extracción de contenidos educativos en Edelvives y ByME. Busca, filtra y extrae enunciados masivamente, exportando listas .txt y documentos Word (.docx).

# Automation Suite

Esta es una suite de herramientas de automatización RPA (Robotic Process Automation) diseñada para agilizar la gestión de contenidos educativos en las plataformas **Edelvives Digital Plus** y **ByME Digital**. 

El proyecto transforma horas de trabajo manual (búsqueda, copiado y pegado de enunciados) en un proceso automatizado de unos pocos minutos, utilizando una interfaz web amigable.

## Características

La aplicación se divide en dos módulos principales integrados en una única interfaz web:

1. **📋 Recolector de Códigos:**
   * Accede al backoffice de la plataforma seleccionada.
   * Navega dinámicamente a través de la paginación.
   * Filtra automáticamente por tipo de contenido (`Question`).
   * Extrae y compila todos los códigos asociados a un libro (código padre) en un archivo `.txt` limpio y ordenado alfabéticamente.

2. **📝 Extractor de Enunciados a Word:**
   * Lee el archivo `.txt` generado por el Recolector.
   * Localiza cada contenido en la plataforma y accede a su entorno de edición interno.
   * Extrae el HTML oculto de los enunciados (saltándose las limitaciones de la interfaz de usuario).
   * Genera un documento Microsoft Word (`.docx`) formateado de forma nativa, conservando etiquetas estructurales (negritas, cursivas, subrayados).
   * Sistema anti-fallos: Si una actividad está vacía o no existe, el robot lo documenta y continúa sin interrumpir el proceso.

## 🛠️ Stack Tecnológico

* **[Python 3](https://www.python.org/):** Lenguaje principal del proyecto.
* **[Streamlit](https://streamlit.io/):** Framework utilizado para renderizar la interfaz de usuario (UI) web de forma nativa.
* **[Playwright](https://playwright.dev/python/):** Motor de automatización web (Headless Chromium) para el control del navegador y simulación de interacciones humanas.
* **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/):** Parseo y limpieza de estructuras HTML complejas.
* **[python-docx](https://python-docx.readthedocs.io/):** Creación y maquetación de los documentos finales.

## ☁️ Uso en la Nube (Streamlit Community Cloud)

Este proyecto está preparado para ser desplegado directamente en la nube. Gracias a esto, los usuarios finales no necesitan instalar Python ni ningún navegador en sus ordenadores. 

1. El servidor lee el archivo `requirements.txt`.
2. Las librerías y dependencias (incluyendo los binarios del navegador de Playwright) se instalan automáticamente en el backend.
3. El usuario final solo necesita abrir la URL pública en su navegador, ingresar sus credenciales e interactuar con la interfaz gráfica.

---
*Desarrollado para optimizar el flujo de trabajo en la gestión y revisión de contenidos digitales.*
