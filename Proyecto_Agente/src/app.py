import streamlit as st
import pandas as pd
import os
import time
from io import StringIO
import sys
from io_utils import read_any
from eda import (
    validate_eda, plot_length_distribution, plot_q3_distribution, plot_nonstd_aa_pie,
    plot_resolution_distribution, plot_rfactor_distribution, plot_experimental_methods, plot_length_vs_resolution
)
from report import generate_report, generate_pdf_report
from mail import send_email
from agent import ProteinAnalysisAgent
from dotenv import load_dotenv


# Cargar variables de entorno desde el archivo .env
# Esto debe hacerse al principio del script
load_dotenv()
st.set_page_config(page_title="Agente de Análisis de Proteínas", page_icon="🔬", layout="wide")

# ---- Constantes y Rutas ----
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
EXAMPLE_FILENAME = "2018-06-06-pdb-intersect-pisces.csv"
EXAMPLE_FILE_PATH = os.path.join(_PROJECT_ROOT, EXAMPLE_FILENAME)

# ---- Estado ----
def initialize_state():
    """Inicializa el estado de la sesión si es necesario."""
    defaults = {"df": None, "messages": [], "eda_ok": False, "ran": False, "agent": None, "eda_context": "", "report_pdf": None}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_state()
            
# ---- Sidebar: Panel de proyecto ----
st.sidebar.title("🔬 Agente de Análisis")
st.sidebar.markdown(
    """
    **Autor:** [Juan Felipe Cardona](https://www.linkedin.com/in/juan-felipe-c-8a010b121/)
    **Repositorio:** [GitHub](https://github.com/Vagarh/AI-Master-EAFIT)

    ---
    Esta herramienta combina análisis de datos y un agente de IA para explorar datasets de proteínas.
    """)
with st.sidebar.expander("📚 Más información"):
    st.markdown("""
        - **Análisis Exploratorio (EDA):** Genera visualizaciones automáticas sobre la distribución de secuencias, estructuras secundarias y calidad de los datos.
        - **Agente Conversacional:** Responde preguntas sobre tus datos y utiliza herramientas externas como **BLAST** y **PDB** para obtener información enriquecida.
        - **Reportes:** Descarga o envía por email un informe completo en PDF.
        - **Modelo LLM:** `deepseek-ai/DeepSeek-R1` (vía Hugging Face).
    """)
email_to = st.sidebar.text_input("Enviar resultados a (opcional)")

st.sidebar.markdown("---")

def reset_session():
    """Limpia el estado de la sesión y reinicia la aplicación."""
    st.session_state.clear()
    initialize_state()
    st.rerun()

if st.sidebar.button("🔄 Restablecer Sesión"):
    reset_session()

# ---- Inicialización del Agente (desde variables de entorno) ----
if "agent" not in st.session_state or st.session_state.agent is None:
    try:
        # El constructor de ProteinAnalysisAgent buscará la variable de entorno HUGGING_FACE_API_KEY
        st.session_state.agent = ProteinAnalysisAgent()
    except ValueError as e:
        # Si no se encuentra la API key, el agente no se crea.
        # La UI mostrará que el agente no está listo.
        st.session_state.agent = None

# ---- Carga de datos ----
st.header("1. Carga tu Dataset")

with st.expander("Ver requisitos del formato y descargar plantilla"):
    st.markdown("""
    Para que el análisis funcione correctamente, tu archivo (CSV, XLS o XLSX) debe contener, como mínimo, las siguientes columnas:
    - `seq`: La secuencia de aminoácidos.
    - `sst3`: La secuencia de estructura secundaria en 3 estados (H, E, C).
    - `sst8`: La secuencia de estructura secundaria en 8 estados.
    - `len`: La longitud de la secuencia (numérico).
    - `has_nonstd_aa`: Un valor booleano (`True`/`False`) que indica si la secuencia contiene aminoácidos no estándar.

    **La forma más fácil de empezar es usar nuestro archivo de ejemplo como plantilla.**
    """)
    if os.path.exists(EXAMPLE_FILE_PATH):
        with open(EXAMPLE_FILE_PATH, "rb") as fp:
            st.download_button(label="📥 Descargar plantilla (.csv)", data=fp, file_name=f"plantilla_{EXAMPLE_FILENAME}", mime="text/csv",
                               help="Descarga el archivo de ejemplo para usarlo como base para tus propios datos.")

data_options = ["Subir un archivo", "Usar datos de ejemplo"]
data_choice = st.radio("Selecciona la fuente de datos:", data_options)

if data_choice == "Subir un archivo":
    file = st.file_uploader(
        "Sube un .csv, .xls o .xlsx",
        type=["csv", "xls", "xlsx"],
        accept_multiple_files=False
    )
    if file:
        st.session_state.df = read_any(file)
        if st.session_state.df is not None:
            st.success(f"Dataset cargado: {st.session_state.df.shape[0]} filas x {st.session_state.df.shape[1]} columnas")
    else:
        # Clear dataframe if no file is uploaded in this mode
        st.session_state.df = None
else:  # "Usar datos de ejemplo"
    if os.path.exists(EXAMPLE_FILE_PATH):
        st.info(
            f"Se cargará el dataset de ejemplo '{EXAMPLE_FILENAME}'. Puedes encontrar este archivo en el repositorio del proyecto."
        )
        st.session_state.df = pd.read_csv(EXAMPLE_FILE_PATH)
        if st.session_state.df is not None:
            st.success(
                f"Dataset de ejemplo cargado: {st.session_state.df.shape[0]} filas x {st.session_state.df.shape[1]} columnas"
            )
    else:
        st.error(f"No se encontró el archivo de ejemplo. Se esperaba en: {EXAMPLE_FILE_PATH}")
        st.session_state.df = None

# ---- Reglas de habilitación ----
agent_ready = st.session_state.agent is not None
ready = st.session_state.df is not None and agent_ready

with st.container(border=True):
    st.markdown("##### Estado del Sistema")
    col1, col2 = st.columns(2)
    if st.session_state.df is not None:
        col1.success("✅ Dataset Cargado", icon="📁")
    else:
        col1.warning("⏳ Dataset Pendiente", icon="📁")

    if agent_ready:
        col2.success("✅ Agente de IA Listo", icon="🤖")
    else:
        col2.error("❌ Agente No Configurado", icon="🤖")

if not agent_ready:
    st.warning("La API Key de Hugging Face no está configurada. Para habilitar el agente, define la variable de entorno `HUGGING_FACE_API_KEY` en tu sistema o en un archivo `.env`.")

# ---- Flujo Principal de la App ----

# 1. Vista de Configuración (si el análisis no se ha ejecutado)
if not st.session_state.ran:
    st.header("2. Inicia el Análisis")
    st.info("Una vez que el dataset y el agente estén listos, haz clic en el botón para comenzar.")
    
    start = st.button("🚀 Iniciar Análisis", disabled=not ready, type="primary", help="Haz clic aquí para procesar el dataset y activar el agente.")
    if start and ready:
        with st.spinner("Procesando dataset y preparando el agente..."):
            df = st.session_state.df
            st.session_state.eda_ok = validate_eda(df)
            
            # Generar contexto de EDA para el agente
            if st.session_state.eda_ok:
                buffer = StringIO()
                df.info(buf=buffer)
                info_str = buffer.getvalue()
                desc_str = df.describe().to_string()
                st.session_state.eda_context = f"Resumen del Dataset:\n{info_str}\n\nEstadísticas Descriptivas:\n{desc_str}"

            # --- Mensaje de bienvenida del agente ---
            if st.session_state.agent and st.session_state.eda_ok:
                welcome_message = (
                    "¡Hola! Soy tu asistente de análisis de proteínas. He procesado tu dataset y estoy listo para ayudarte. "
                    "Tengo acceso a las siguientes herramientas:\n"
                    "- **Análisis de Datos:** Puedo responder preguntas sobre el dataset que cargaste.\n"
                    "- **Búsqueda BLAST:** Puedo tomar una secuencia y buscarla en la base de datos de NCBI.\n"
                    "- **Protein Data Bank (PDB):** Puedo buscar información sobre una estructura si me das su ID de 4 caracteres.\n\n"
                    "Puedes explorar el dashboard o hacerme una pregunta. ¿En qué te puedo ayudar?"
                )
                st.session_state.messages = [{"role": "assistant", "content": welcome_message}]
            
            st.session_state.ran = True
        
        st.success("¡Análisis completado!")
        time.sleep(1)
        st.rerun()

# 2. Vista de Resultados (si el análisis ya se ejecutó)
else:
    # ---- Tabs: Chat, Dashboard y EDA ----
    tab_chat, tab_dashboard, tab_eda = st.tabs(["💬 Chat con Agente", "📊 Dashboard de Insights", "📄 Exploración de Datos (EDA)"])

    with tab_chat:
        st.subheader("💬 Conversa con el Agente")
        for m in st.session_state.messages:
            with st.chat_message(m['role']):
                st.markdown(m['content'])

        prompt = None
        chat_disabled = not st.session_state.ran or not st.session_state.agent

        if not chat_disabled:
            st.markdown("**Sugerencias de preguntas:**")
            predefined_questions = [
                "Resume las características principales del dataset.",
                "¿Cuál es la longitud promedio de las secuencias?",
                "Toma la primera secuencia y búscala en BLAST.",
                "Busca información del PDB ID '2HHB' (hemoglobina)."
            ]
            cols = st.columns(len(predefined_questions))
            for i, question in enumerate(predefined_questions):
                if cols[i].button(question, use_container_width=True, help=f"Preguntar: {question}"):
                    prompt = question

        if chat_input := st.chat_input("O escribe tu propia pregunta...", disabled=chat_disabled):
            prompt = chat_input

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Pensando..."):
                    chat_history = st.session_state.messages[:-1]
                    assistant_reply = st.session_state.agent.chat(
                        context=st.session_state.eda_context, user_question=prompt, chat_history=chat_history
                    )
                    st.markdown(assistant_reply)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})

    with tab_dashboard:
        if st.session_state.eda_ok:
            df = st.session_state.df
            st.subheader("📊 Dashboard Interactivo de Insights")
            st.markdown("Utiliza los filtros para explorar subconjuntos de datos. Los gráficos y métricas se actualizarán automáticamente.")

            with st.container(border=True):
                st.markdown("#### ⚙️ Filtros Interactivos")
                min_len, max_len = int(df['len'].min()), int(df['len'].max())
                selected_len_range = st.slider("Filtrar por longitud de secuencia:", min_value=min_len, max_value=max_len, value=(min_len, max_len))

            df_filtered = df[(df['len'] >= selected_len_range[0]) & (df['len'] <= selected_len_range[1])]
            st.info(f"Mostrando **{len(df_filtered):,}** de **{len(df):,}** secuencias según los filtros aplicados.")

            if not df_filtered.empty:
                col1, col2, col3 = st.columns(3)
                col1.metric("Secuencias (filtrado)", f"{df_filtered.shape[0]:,}")
                col2.metric("Longitud Promedio", f"{df_filtered['len'].mean():.0f} AA")
                col3.metric("Con AA No Estándar", f"{df_filtered['has_nonstd_aa'].sum() / len(df_filtered):.1%}")

                st.markdown("#### Distribución de la Longitud de las Secuencias")
                st.pyplot(plot_length_distribution(df_filtered))

                col_viz1, col_viz2 = st.columns(2)
                with col_viz1:
                    st.markdown("#### Frecuencia de Estructuras (Q3)")
                    st.pyplot(plot_q3_distribution(df_filtered))
                with col_viz2:
                    st.markdown("#### Proporción de Aminoácidos No Estándar")
                    st.pyplot(plot_nonstd_aa_pie(df_filtered))
                
                st.markdown("---")
                st.markdown("### Análisis de Calidad Estructural")
                if 'resolution' in df_filtered.columns:
                    st.markdown("#### Distribución de Resoluciones")
                    st.pyplot(plot_resolution_distribution(df_filtered))
                if 'R-factor' in df_filtered.columns:
                    st.markdown("#### Distribución del R-factor")
                    st.pyplot(plot_rfactor_distribution(df_filtered))
                if 'Exptl.' in df_filtered.columns:
                    st.markdown("#### Métodos Experimentales")
                    st.pyplot(plot_experimental_methods(df_filtered))
                if 'len' in df_filtered.columns and 'resolution' in df_filtered.columns:
                    st.markdown("#### Longitud vs. Resolución")
                    st.pyplot(plot_length_vs_resolution(df_filtered))
            else:
                st.warning("No hay datos que mostrar con los filtros seleccionados.")
        else:
            st.warning("Dashboard no disponible: faltan columnas mínimas para el análisis.")

    with tab_eda:
        if st.session_state.eda_ok:
            df = st.session_state.df
            st.subheader("📄 Exploración Detallada de Datos (EDA)")
            st.markdown("Aquí puedes inspeccionar la estructura y los valores del dataset. Por defecto se muestra una vista previa de las primeras 20 filas.")
            
            st.dataframe(df.head(20))

            with st.expander("Ver dataset completo"):
                st.dataframe(df)

            with st.expander("Ver detalles estadísticos"):
                st.markdown(f"**Dimensiones:** {df.shape[0]} filas x {df.shape[1]} columnas")
                st.markdown("**Resumen de valores nulos por columna**")
                st.write(df.isna().sum().to_frame("nulos"))
                st.markdown("**Estadísticas descriptivas de columnas numéricas**")
                st.write(df.select_dtypes("number").describe().T)
        else:
            st.warning("Exploración no disponible: faltan columnas mínimas {'seq','sst3','sst8','len','has_nonstd_aa'}")

    st.header("3. Obtén tus Resultados")
    # Generar el PDF solo una vez y guardarlo en caché en el estado de la sesión para mejorar el rendimiento
    if st.session_state.report_pdf is None:
        with st.spinner("Generando reporte PDF por primera vez..."):
            st.session_state.report_pdf = generate_pdf_report(st.session_state.eda_ok, st.session_state.df)
    report_content_pdf = st.session_state.report_pdf

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(label="📥 Descargar Reporte (.pdf)", data=report_content_pdf, file_name="reporte_analisis_proteinas.pdf", mime="application/pdf", help="Descarga un informe completo en formato PDF con todos los análisis y gráficos.")
    with col2:
        if st.button("📧 Enviar por Email"):
            if not email_to:
                st.warning("Por favor, introduce una dirección de correo en el panel de la izquierda.")
            else:
                with st.spinner("Enviando correo..."):
                    email_body = "Adjunto encontrarás el reporte de análisis de proteínas generado por el agente inteligente."
                    ok, message = send_email(email_to, "Reporte de Análisis de Proteínas", email_body, attachment_data=report_content_pdf, attachment_filename="reporte.pdf", attachment_mimetype="application/pdf")
                    if ok:
                        st.success(message)
                    else:
                        st.error(message)
