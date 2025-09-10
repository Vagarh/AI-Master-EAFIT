# Guion para Sustentación (5 Minutos)

**Título:** Aplicación Inteligente para el Análisis de Estructuras Secundarias de Proteínas

---

### 1. Introducción (30 segundos)

*   **Problema:** Investigadores y estudiantes de biología a menudo manejan grandes datasets de secuencias de proteínas. Extraer insights rápidos y responder preguntas específicas sobre estos datos puede ser un proceso manual y lento.
*   **Solución:** Hemos desarrollado una aplicación web interactiva que automatiza el análisis exploratorio de datos (EDA) y lo integra con un agente de IA conversacional para responder preguntas complejas sobre los datos y conceptos biológicos relacionados.
*   **Objetivo:** Democratizar el acceso a la información contenida en datos de secuencias peptídicas.

---

### 2. Arquitectura y Decisiones de Diseño (1 minuto 30 segundos)

*   **Visión General de la Arquitectura (Frontend-Backend desacoplado):**
    *   **Frontend:** **Streamlit**, elegido por su rapidez para crear aplicaciones de datos interactivas con Python puro.
    *   **Procesamiento de Datos:** **Pandas y Matplotlib/Seaborn**, el estándar de la industria para manipulación y visualización de datos.
    *   **Cerebro (IA):** **LangChain + Hugging Face**, nos permite orquestar un modelo de lenguaje open-source (`google/flan-t5-large`) de forma gratuita y flexible.

*   **Estructura del Código (Modular y Escalable):**
    *   `streamlit.py`: Gestiona la UI y el flujo de la aplicación. No contiene lógica de negocio.
    *   `eda.py`: Contiene todas las funciones de análisis y visualización. Es reutilizable.
    *   `agent.py`: Abstrae toda la complejidad de la IA. Se encarga de la configuración del LLM y el *prompt engineering*.

*   **Decisión de Diseño Clave: Agente Contextualizado**
    *   En lugar de usar un LLM genérico, creamos un **agente especializado**. Le "inyectamos" un resumen del EDA del *dataset cargado* directamente en su prompt.
    *   **¿Por qué?** Esto permite que el agente no solo responda sobre biología general, sino que **contextualice sus respuestas con los datos específicos que el usuario está viendo**, por ejemplo: "*En tu dataset, la hélice alfa (H) es la estructura más común, presente en el 45% de las secuencias...*"

---

### 3. Desafíos Técnicos y Soluciones (1 minuto)

*   **Desafío 1: Acceso a Datos y Flexibilidad.**
    *   **Problema:** No podíamos depender de un único dataset estático.
    *   **Solución:** Implementamos un cargador de archivos en Streamlit. La aplicación se adapta a cualquier CSV que siga la estructura, lo que la hace muy versátil.

*   **Desafío 2: Integración Segura y Eficiente del LLM.**
    *   **Problema:** Evitar exponer API keys y prevenir que el agente se recargue con cada interacción del usuario.
    *   **Solución:** Usamos variables de entorno para la API key (una práctica segura) y `st.session_state` de Streamlit para guardar en caché la instancia del agente, mejorando drásticamente el rendimiento.

*   **Desafío 3: Prompt Engineering.**
    *   **Problema:** Lograr que el LLM respondiera de forma útil y basada en el contexto.
    *   **Solución:** Diseñamos una plantilla de prompt muy específica que le da al modelo un rol ("*Eres un experto en biología...*"), le proporciona el contexto del EDA y formatea claramente la pregunta del usuario.

---

### 4. Conclusión y Pasos Futuros (30 segundos)

*   **Logro:** Hemos creado una herramienta funcional que combina EDA y IA conversacional para el análisis de proteínas, lista para ser desplegada en la nube.
*   **Futuro:**
    *   **Expansión del Agente:** Conectarlo a herramientas como BLAST para búsquedas de secuencias en tiempo real.
    *   **Visualizaciones Avanzadas:** Integrar visores 3D de moléculas (ej. `py3Dmol`).
    *   **Soporte de Más Formatos:** Aceptar archivos FASTA además de CSV.
