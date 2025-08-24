import streamlit as st
import pandas as pd
from io import StringIO
import sys
from io_utils import read_any
from eda import validate_eda, plot_length_distribution, plot_q3_distribution, plot_nonstd_aa_pie
from report import generate_report, generate_pdf_report
from mail import send_email
from agent import ProteinAnalysisAgent
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
# Esto debe hacerse al principio del script
load_dotenv()
st.set_page_config(page_title="Agente de Análisis de Proteínas", layout="wide")

# ---- Estado ----
if "df" not in st.session_state: st.session_state.df = None
if "messages" not in st.session_state: st.session_state.messages = []
if "eda_ok" not in st.session_state: st.session_state.eda_ok = False
if "ran" not in st.session_state: st.session_state.ran = False
if "agent" not in st.session_state: st.session_state.agent = None
if "eda_context" not in st.session_state: st.session_state.eda_context = ""

# ---- Sidebar: Panel de proyecto ----
st.sidebar.title("Agente de Análisis de Proteínas")
st.sidebar.markdown("""
**Autor:** Helios
**Funcionalidad:** Carga dataset, EDA básico y chat con agente.
**Dominio:** Secuencias y estructuras secundarias (Q3/Q8).
""")

api_key = st.sidebar.text_input("HuggingFace API Key", type="password", help="Se requiere para habilitar el análisis.")
email_to = st.sidebar.text_input("Enviar resultados a (opcional)")

st.sidebar.markdown("---")
if st.sidebar.button("Restablecer"):
    st.session_state.df = None
    st.session_state.messages = []
    st.session_state.eda_ok = False
    st.session_state.ran = False
    st.session_state.agent = None
    st.session_state.eda_context = ""
    st.rerun()

# ---- Carga de datos ----
st.header("Carga de dataset")
file = st.file_uploader("Sube un .csv, .xls o .xlsx", type=["csv","xls","xlsx"])

if file:
    st.session_state.df = read_any(file)
    if st.session_state.df is not None:
        st.success(f"Dataset cargado: {st.session_state.df.shape[0]} filas x {st.session_state.df.shape[1]} columnas")

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
    
    st.success("Análisis iniciado")

# ---- Tabs: Chat y EDA ----
tab_chat, tab_eda = st.tabs(["Chat del agente", "EDA"])

with tab_chat:
    st.subheader("Historial")
    for m in st.session_state.messages:
        with st.chat_message(m['role']):
            st.markdown(m['content'])
            
    user_msg = st.chat_input("Escribe tu mensaje", disabled=(not st.session_state.ran or not st.session_state.agent))
    
    if user_msg:
        st.session_state.messages.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)
            
        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                if st.session_state.agent:
                    assistant_reply = st.session_state.agent.chat(st.session_state.eda_context, user_msg)
                    st.markdown(assistant_reply)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                else:
                    st.error("El agente no está inicializado. Por favor, introduce una API key válida.")

with tab_eda:
    if not st.session_state.ran:
        st.info("EDA no ejecutado. Carga dataset y API key, luego pulsa Iniciar análisis.")
    else:
        if st.session_state.eda_ok:
            df = st.session_state.df
            st.markdown("**EDA disponible**")
            st.markdown(f"- Filas: {df.shape[0]} | Columnas: {df.shape[1]}")
            st.markdown("**Vista previa**")
            st.dataframe(df.head(20))
            st.markdown("**Nulos por columna**")
            st.write(df.isna().sum().to_frame("nulos"))
            st.markdown("**Estadísticos**")
            st.write(df.select_dtypes("number").describe().T)

            # --- Visualizaciones ---
            st.markdown("---")
            st.subheader("Visualizaciones del Dataset")

            # Plot 1: Distribución de longitud
            st.markdown("#### Distribución de la Longitud de las Secuencias")
            fig_len = plot_length_distribution(df)
            st.pyplot(fig_len)

            # Plots 2 y 3 en columnas
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Frecuencia de Estructuras (Q3)")
                fig_q3 = plot_q3_distribution(df)
                st.pyplot(fig_q3)
            with col2:
                st.markdown("#### Proporción de Aminoácidos No Estándar")
                fig_pie = plot_nonstd_aa_pie(df)
                st.pyplot(fig_pie)
        else:
            st.warning("EDA no disponible: faltan columnas mínimas {'seq','sst3','sst8','len','has_nonstd_aa'}")

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
