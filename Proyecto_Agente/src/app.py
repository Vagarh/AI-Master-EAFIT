import streamlit as st
import pandas as pd
import os
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
st.set_page_config(page_title="Agente de Análisis de Proteínas", layout="wide")

# ---- Constantes y Rutas ----
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
EXAMPLE_FILENAME = "2018-06-06-pdb-intersect-pisces.csv"
EXAMPLE_FILE_PATH = os.path.join(_PROJECT_ROOT, EXAMPLE_FILENAME)

# ---- Estado ----
def initialize_state():
    """Inicializa el estado de la sesión si es necesario."""
    defaults = {"df": None, "messages": [], "eda_ok": False, "ran": False, "agent": None, "eda_context": ""}
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_state()
            
# ---- Sidebar: Panel de proyecto ----
st.sidebar.title("Agente de Análisis de Proteínas")
st.sidebar.markdown(
    """
    **Autor:** [Juan Felipe Cardona](https://www.linkedin.com/in/juan-felipe-c-8a010b121/)
    **Repositorio:** [GitHub](https://github.com/Vagarh/AI-Master-EAFIT)

    ---

    Esta herramienta permite el análisis interactivo de datasets de proteínas. 
    Carga tus datos, explora las visualizaciones del EDA y conversa con un agente 
    de IA para obtener insights sobre la estructura y composición de las secuencias.

    ---
    **Tecnologías:**
    - `Streamlit`, `Pandas`, `Matplotlib`, `Seaborn`, `fpdf2`, `Biopython`
    
    BLAST para búsqueda de secuencias.

    **Modelo LLM:** `deepseek-ai/DeepSeek-R1` (vía Hugging Face)
    """
)
api_key = st.sidebar.text_input("HuggingFace API Key", type="password", help="Se requiere para habilitar el análisis.")
email_to = st.sidebar.text_input("Enviar resultados a (opcional)")

st.sidebar.markdown("---")

def reset_session():
    """Limpia el estado de la sesión y reinicia la aplicación."""
    st.session_state.clear()
    initialize_state()
    st.rerun()

if st.sidebar.button("Restablecer"):
    reset_session()

# ---- Carga de datos ----
st.header("Carga de dataset")

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
ready = st.session_state.df is not None and bool(api_key)

col1, col2 = st.columns(2)
with col1:
    st.metric("Dataset", "OK" if st.session_state.df is not None else "Pendiente")
with col2:
    st.metric("API key", "OK" if api_key else "Pendiente")

# ---- Inicialización del Agente ----
if api_key and not st.session_state.agent:
    try:
        st.session_state.agent = ProteinAnalysisAgent(api_key=api_key)
        st.info("¡Agente listo! Ahora puedes interactuar con tus datos.")
    except ValueError as e:
        st.error(e)

# ---- Botón de análisis ----
start = st.button("Iniciar análisis", disabled=not ready)
if start and ready:
    df = st.session_state.df
    st.session_state.eda_ok = validate_eda(df)
    st.session_state.ran = True

    # Generar contexto de EDA para el agente
    if st.session_state.eda_ok:
        buffer = StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        desc_str = df.describe().to_string()
        st.session_state.eda_context = f"Resumen del Dataset:\n{info_str}\n\nEstadísticas Descriptivas:\n{desc_str}"

    st.success("Análisis completado. ¡Ya puedes chatear con el agente!")

    # --- Mensaje de bienvenida del agente ---
    # Para mejorar la experiencia de usuario, el agente inicia la conversación
    # en lugar de esperar a que el usuario escriba primero.
    if st.session_state.agent and st.session_state.eda_ok:
        welcome_message = (
            "¡Hola! Soy tu asistente de análisis de proteínas. He procesado tu dataset y estoy listo para ayudarte. "
            "Puedes explorar el Análisis Exploratorio de Datos (EDA) en la otra pestaña o hacerme preguntas directamente. \n\n"
            "**Aquí tienes algunas ideas para empezar:**\n"
            "- '¿Cuál es la longitud promedio de las secuencias?'\n"
            "- 'Resume las características principales del dataset.'\n"
            "- 'Toma la primera secuencia y búscala en BLAST.'"
        )
        st.session_state.messages = [{"role": "assistant", "content": welcome_message}]
# ---- Tabs: Chat, Dashboard y EDA ----
tab_chat, tab_dashboard, tab_eda = st.tabs(["Chat del agente", "Dashboard de Insights", "Exploración de Datos (EDA)"])

with tab_chat:
    st.subheader("Historial")
    for m in st.session_state.messages:
        with st.chat_message(m['role']):
            st.markdown(m['content'])
            
    user_msg = st.chat_input("Escribe tu mensaje", disabled=(not st.session_state.ran or not st.session_state.agent))
    
    with st.expander("✨ Descubre las herramientas del agente"):
        st.info(
            "El agente puede usar herramientas externas como **BLAST** para responder preguntas "
            "que van más allá de los datos cargados."
        )
        st.markdown("#### Prueba a preguntarle:")
        st.code("Busca en BLAST la secuencia MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVFVPPDE y resume los hallazgos.")
        st.markdown("O también puedes preguntarle sobre una secuencia de tu propio dataset:")
        st.code("Toma la primera secuencia del dataset, busca en BLAST y dime a qué se parece.")

    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)
            
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                if st.session_state.agent:
                    # Pasamos el historial de chat (todos los mensajes excepto el último del usuario)
                    # para que el agente tenga memoria de la conversación.
                    chat_history = st.session_state.messages[:-1]
                    assistant_reply = st.session_state.agent.chat(
                        context=st.session_state.eda_context, user_question=user_msg, chat_history=chat_history
                    )
                    st.markdown(assistant_reply)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                else:
                    st.error("El agente no está inicializado. Por favor, introduce una API key válida.")

with tab_dashboard:
    if not st.session_state.ran:
        st.info("Ejecuta el análisis para ver el dashboard de insights.")
    else:
        if st.session_state.eda_ok:
            df = st.session_state.df
            st.subheader("Dashboard de Insights del Dataset")
            st.markdown("Utiliza los filtros para explorar subconjuntos de datos. Los gráficos y métricas se actualizarán automáticamente.")

            # --- FILTROS DEL DASHBOARD ---
            st.markdown("---")
            st.markdown("#### Filtros Interactivos")
            
            # Filtro por longitud de secuencia
            min_len, max_len = int(df['len'].min()), int(df['len'].max())
            selected_len_range = st.slider(
                "Filtrar por longitud de secuencia:",
                min_value=min_len,
                max_value=max_len,
                value=(min_len, max_len)
            )

            # Aplicar filtros al dataframe
            df_filtered = df[
                (df['len'] >= selected_len_range[0]) & (df['len'] <= selected_len_range[1])
            ]
            
            st.info(f"Mostrando **{len(df_filtered):,}** de **{len(df):,}** secuencias según los filtros aplicados.")
            st.markdown("---")

            # Métricas clave (usando el dataframe filtrado)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Secuencias (filtrado)", f"{df_filtered.shape[0]:,}")

            if not df_filtered.empty:
                avg_len = f"{df_filtered['len'].mean():.0f} AA"
                non_std_pct = f"{df_filtered['has_nonstd_aa'].sum() / len(df_filtered):.1%}"
                
                col2.metric("Longitud Promedio", avg_len)
                col3.metric("Con AA No Estándar", non_std_pct)

                # --- Visualizaciones de Secuencia (usando el dataframe filtrado) ---
                st.markdown("#### Distribución de la Longitud de las Secuencias")
                fig_len = plot_length_distribution(df_filtered)
                st.pyplot(fig_len)

                col_viz1, col_viz2 = st.columns(2)
                with col_viz1:
                    st.markdown("#### Frecuencia de Estructuras (Q3)")
                    fig_q3 = plot_q3_distribution(df_filtered)
                    st.pyplot(fig_q3)
                with col_viz2:
                    st.markdown("#### Proporción de Aminoácidos No Estándar")
                    fig_pie = plot_nonstd_aa_pie(df_filtered)
                    st.pyplot(fig_pie)
                
                # --- Visualizaciones de Calidad Estructural ---
                st.markdown("---")
                st.markdown("### Análisis de Calidad Estructural")
                st.markdown("Estos gráficos analizan las propiedades experimentales de las estructuras en el dataset.")

                # Verificar si las columnas necesarias existen antes de plotear
                if 'resolution' in df_filtered.columns:
                    st.markdown("#### Distribución de Resoluciones")
                    fig_res = plot_resolution_distribution(df_filtered)
                    st.pyplot(fig_res)
                
                if 'R-factor' in df_filtered.columns:
                    st.markdown("#### Distribución del R-factor")
                    fig_r = plot_rfactor_distribution(df_filtered)
                    st.pyplot(fig_r)

                if 'Exptl.' in df_filtered.columns:
                    st.markdown("#### Métodos Experimentales")
                    fig_exp = plot_experimental_methods(df_filtered)
                    st.pyplot(fig_exp)

                if 'len' in df_filtered.columns and 'resolution' in df_filtered.columns:
                    st.markdown("#### Longitud vs. Resolución")
                    fig_len_res = plot_length_vs_resolution(df_filtered)
                    st.pyplot(fig_len_res)
            else:
                st.warning("No hay datos que mostrar con los filtros seleccionados.")
        else:
            st.warning("Dashboard no disponible: faltan columnas mínimas para el análisis.")

with tab_eda:
    if not st.session_state.ran:
        st.info("Ejecuta el análisis para explorar los datos en detalle.")
    else:
        if st.session_state.eda_ok:
            df = st.session_state.df
            st.subheader("Exploración Detallada de Datos")
            st.markdown("Aquí puedes inspeccionar la estructura y los valores del dataset.")
            st.markdown(f"**Dimensiones:** {df.shape[0]} filas x {df.shape[1]} columnas")
            st.markdown("**Vista previa del dataset**")
            st.dataframe(df.head(20))
            st.markdown("**Resumen de valores nulos por columna**")
            st.write(df.isna().sum().to_frame("nulos"))
            st.markdown("**Estadísticas descriptivas de columnas numéricas**")
            st.write(df.select_dtypes("number").describe().T)
        else:
            st.warning("Exploración no disponible: faltan columnas mínimas {'seq','sst3','sst8','len','has_nonstd_aa'}")

# ---- Reporte y envío ----
st.markdown("---")
st.subheader("Resultados")

if not st.session_state.ran:
    st.info("Ejecuta el análisis para poder generar y enviar el reporte.")
else:
    with st.spinner("Generando reporte PDF..."):
        report_content_pdf = generate_pdf_report(st.session_state.eda_ok, st.session_state.df)

    col1, col2 = st.columns(2)

    with col1:
        # --- Botón de descarga ---
        st.download_button(
            label="Descargar reporte (.pdf)",
            data=report_content_pdf,
            file_name="reporte_analisis_proteinas.pdf",
            mime="application/pdf"
        )

    with col2:
        # --- Botón de envío por correo ---
        if st.button("Enviar reporte por email"):
            if not email_to:
                st.warning("Por favor, introduce una dirección de correo en el panel de la izquierda.")
            else:
                with st.spinner("Enviando correo..."):
                    email_body = "Adjunto encontrarás el reporte de análisis de proteínas generado por el agente inteligente."
                    ok, message = send_email(email_to, 
                                             "Reporte de Análisis de Proteínas", 
                                             email_body,
                                             attachment_data=report_content_pdf,
                                             attachment_filename="reporte.pdf",
                                             attachment_mimetype="application/pdf")
                    if ok:
                        st.success(message)
                    else:
                        st.error(message)
