# 🔒 GUÍA DE SEGURIDAD - WebScraper

## Resumen de mejoras de seguridad

Este proyecto ha sido actualizado para **eliminar cualquier riesgo de credenciales hardcodeadas**. 

### ✅ Medidas implementadas:

#### 1. **No hay credenciales hardcodeadas**
   - Las credenciales se solicitan en tiempo de ejecución a través de la interfaz
   - Nunca se guardan ni se registran en el código

#### 2. **Archivo `.env` para configuración**
   - Las URLs de plataformas se centralizan en `config.py`
   - Se pueden personalizar mediante variables de entorno (`.env`)
   - Ejemplo: `.env.example` muestra la estructura

#### 3. **Archivo `.gitignore` protegido**
   - El archivo `.env` está en `.gitignore` (nunca se sube a Git)
   - Archivos de Streamlit secrets también protegidos
   - Archivos `.docx` y `.txt` generados también ignorados

#### 4. **Configuración centralizada** (`config.py`)
   - Todas las URLs y configuración en un lugar
   - Fácil mantenimiento y escalabilidad
   - Fallback a valores por defecto

---

## 🚀 Cómo usar el proyecto de forma segura:

### Opción 1: Con variables de entorno (Recomendado)

1. **Instala dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Copia el archivo de ejemplo:**
   ```bash
   cp .env.example .env
   ```

3. **Personaliza el archivo `.env`** (si es necesario):
   ```env
   URL_EPD=https://publisher.edelvivesdigitalplus.com/
   URL_BYME=https://publisher.bymedigital.com/
   ```

4. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```

### Opción 2: Sin archivo `.env`

El proyecto usa valores por defecto automáticamente si no existe `.env`.

---

## 📋 Archivo `.env.example`

Sirve como plantilla y referencia. **NO debe contener valores reales**.

---

## ⚠️ Checklist de seguridad:

- ✅ No subas el archivo `.env` a Git
- ✅ No compartas credenciales en código
- ✅ Las credenciales se solicitan en la interfaz Streamlit
- ✅ Usa `config.py` para toda configuración centralizada
- ✅ Revisa `.gitignore` para archivos sensibles

---

## 🔐 Para deployments (Streamlit Cloud, etc.)

**En Streamlit Cloud:**
1. Ve a **Settings → Secrets**
2. Agrega tus URLs y configuración ahí
3. Streamlit lo cargará automáticamente

**En otros servidores:**
1. Define variables de entorno en el servidor
2. Usa un archivo `.env` local (nunca en versionamiento)
3. Considera usar gestores de secretos (AWS Secrets, Azure Key Vault, etc.)

---

## 📚 Archivos modificados:

- ✅ `app.py` - Ahora usa `config.py` centralizado
- ✅ `requirements.txt` - Agregado `python-dotenv`
- ✅ `config.py` - **NUEVO** Centralización de configuración
- ✅ `.gitignore` - **NUEVO** Protege archivos sensibles
- ✅ `.env.example` - **NUEVO** Plantilla de entorno

---

**Estado:** ✅ Proyecto seguro - Listo para producción
