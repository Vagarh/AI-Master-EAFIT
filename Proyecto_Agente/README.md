# Agente de Análisis de Proteínas

Una aplicación web interactiva construida con Streamlit que combina Análisis Exploratorio de Datos (EDA) con un agente de IA conversacional para analizar datasets de secuencias de proteínas.

## 📜 Descripción

Esta herramienta está diseñada para ayudar a investigadores, estudiantes y bioinformáticos a obtener insights rápidos de sus datos de proteínas. La aplicación permite:

1.  **Cargar datos** de secuencias de proteínas desde archivos CSV o Excel.
2.  Realizar un **Análisis Exploratorio de Datos (EDA)** automático para visualizar distribuciones, estadísticas y la calidad de los datos.
3.  **Conversar con un agente de IA** que entiende el contexto de los datos cargados.
4.  Utilizar **herramientas bioinformáticas como BLAST** a través del agente para buscar secuencias en bases de datos externas.
5.  **Generar y descargar un reporte** en PDF con los resultados del análisis.
6.  **Enviar el reporte** por correo electrónico.

## ✨ Características Principales

-   **Interfaz Interactiva:** Carga de datos flexible (archivos locales o datos de ejemplo).
-   **EDA Automatizado:** Visualizaciones automáticas de:
    -   Distribución de longitud de secuencias.
    -   Frecuencia de estructuras secundarias (Q3).
    -   Proporción de aminoácidos no estándar.
-   **Agente Conversacional Inteligente:**
    -   Basado en el modelo `deepseek-ai/DeepSeek-R1`.
    -   Contextualizado con los datos del usuario.
    -   Capaz de usar herramientas externas (integración con BLAST).
-   **Generación de Reportes:** Exporta los resultados y gráficos a un documento PDF profesional.
-   **Notificaciones por Email:** Envía el reporte PDF directamente a tu bandeja de entrada.

## 🛠️ Pila Tecnológica

-   **Frontend:** Streamlit
-   **Análisis de Datos:** Pandas, Matplotlib, Seaborn
-   **IA y LLM:** LiteLLM para interactuar con modelos de Hugging Face.
-   **Bioinformática:** Biopython para la integración con BLAST.
-   **Reportes PDF:** fpdf2
-   **Gestión de Dependencias:** `pip` y `requirements.txt`.

## 🚀 Cómo Empezar

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local.

### 1. Prerrequisitos

-   Python 3.8 o superior.
-   Git.

### 2. Clonar el Repositorio

```bash
git clone https://github.com/Vagarh/AI-Master-EAFIT.git
cd AI-Master-EAFIT/Proyecto_Agente
```

### 3. Crear un Entorno Virtual

Es una buena práctica usar un entorno virtual para aislar las dependencias del proyecto.

```bash
# Para macOS/Linux
python3 -m venv env
source env/bin/activate

# Para Windows
python -m venv env
.\env\Scripts\activate
```

### 4. Instalar Dependencias

Instala todas las librerías necesarias desde el archivo `requirements.txt` ubicado en el directorio raíz del repositorio.

```bash
pip install -r ../requirements.txt
```

### 5. Configurar Variables de Entorno

El agente necesita claves de API y configuración SMTP para funcionar completamente.

1.  Crea un archivo `.env` en el directorio raíz del proyecto (`Proyecto_Agente`). Puedes copiar el archivo de ejemplo:

    ```bash
    cp .env.example .env
    ```

2.  Abre el archivo `.env` y añade tus credenciales.

    > **Nota de Seguridad:** Si usas Gmail, necesitas generar una "Contraseña de aplicación" desde la configuración de seguridad de tu cuenta de Google, no uses tu contraseña principal.

### 6. Ejecutar la Aplicación

Una vez que las dependencias y las variables de entorno estén configuradas, puedes iniciar la aplicación Streamlit.

```bash
streamlit run src/app.py
```

La aplicación se abrirá automáticamente en tu navegador web.

## 📂 Estructura del Proyecto

El código está organizado de manera modular para facilitar su mantenimiento y escalabilidad.

```
Proyecto_Agente/
├── src/
│   ├── __init__.py      # Inicializador del paquete
│   ├── agent.py         # Lógica del agente de IA (LLM, herramientas)
│   ├── app.py           # Aplicación principal de Streamlit (UI)
│   ├── eda.py           # Funciones para el análisis y visualización de datos
│   ├── io_utils.py      # Utilidades para leer archivos
│   ├── mail.py          # Lógica para el envío de correos
│   ├── report.py        # Generación de reportes en PDF
│   └── tools.py         # Herramientas externas (ej. BLAST)
├── .env.example         # Plantilla para variables de entorno
└── README.md            # Este archivo
```
