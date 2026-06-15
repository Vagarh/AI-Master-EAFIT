"""
Configuración centralizada para el Agente de Análisis de Proteínas
"""
import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Archivos de ejemplo
EXAMPLE_FILENAME = "2018-06-06-pdb-intersect-pisces.csv"
EXAMPLE_FILE_PATH = PROJECT_ROOT / EXAMPLE_FILENAME

# Configuración de la aplicación
APP_CONFIG = {
    "page_title": "🔬 Agente de Análisis de Proteínas",
    "page_icon": "🔬",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Configuración del modelo
MODEL_CONFIG = {
    "model_name": "huggingface/together/deepseek-ai/DeepSeek-R1",
    "api_key_env": "HUGGING_FACE_API_KEY",
    "max_tokens": 4000,
    "temperature": 0.1,
    "timeout": 60
}

# Columnas requeridas para el análisis
REQUIRED_COLUMNS = {
    "seq", "sst3", "sst8", "len", "has_nonstd_aa"
}

# Configuración de visualizaciones
VIZ_CONFIG = {
    "color_palette": "viridis",
    "figure_size": (10, 6),
    "dpi": 100,
    "style": "whitegrid"
}

# Configuración de email
EMAIL_CONFIG = {
    "smtp_host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", 587)),
    "smtp_user": os.getenv("SMTP_USER"),
    "smtp_pass": os.getenv("SMTP_PASS")
}

# Mensajes de la aplicación
MESSAGES = {
    "welcome": """
    ¡Hola! 👋 Soy tu asistente especializado en análisis de proteínas. 
    
    He procesado tu dataset y estoy listo para ayudarte con:
    
    🔬 **Análisis de Datos:** Respondo preguntas sobre tu dataset
    🧬 **Búsqueda BLAST:** Busco secuencias similares en NCBI
    📚 **Consulta PDB:** Obtengo información de estructuras cristalográficas
    
    ¿En qué te puedo ayudar hoy?
    """,
    
    "no_api_key": """
    ⚠️ **Configuración Requerida**
    
    Para usar el agente de IA, necesitas configurar tu API Key de Hugging Face:
    
    1. Visita: https://huggingface.co/settings/tokens
    2. Crea un token de acceso
    3. Añádelo como variable de entorno: `HUGGING_FACE_API_KEY`
    
    O crea un archivo `.env` en el directorio del proyecto.
    """,
    
    "dataset_requirements": """
    📋 **Requisitos del Dataset**
    
    Tu archivo debe contener estas columnas mínimas:
    - `seq`: Secuencia de aminoácidos
    - `sst3`: Estructura secundaria (3 estados: H, E, C)
    - `sst8`: Estructura secundaria (8 estados)
    - `len`: Longitud de la secuencia
    - `has_nonstd_aa`: Aminoácidos no estándar (True/False)
    
    **Formatos soportados:** CSV, XLS, XLSX
    """
}