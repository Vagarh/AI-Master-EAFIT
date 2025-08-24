import streamlit as st
import pandas as pd
from io import StringIO
import sys
from io_utils import read_any
from eda import validate_eda
from report import generate_report
from mail import send_email
from agent import ProteinAnalysisAgent

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

api_key = st.sidebar.text_input("API key", type="password", help="Se requiere para habilitar el análisis.")
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
        st.session_state.agent = ProteinAnalysisAgent()
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
        else:
            st.warning("EDA no disponible: faltan columnas mínimas {'seq','sst3','sst8','len','has_nonstd_aa'}")

# ---- Reporte y envío ----
st.markdown("---")
st.subheader("Resultados")
report_btn = st.button("Generar reporte descargable")
if report_btn and st.session_state.ran:
    report_content = generate_report(st.session_state.eda_ok, st.session_state.df)
    st.download_button("Descargar reporte (.txt)", data=report_content, file_name="reporte.txt")

send_btn = st.button("Enviar reporte por email")
if send_btn:
    if not email_to:
        st.error("Falta correo destino.")
    elif not st.session_state.ran:
        st.error("Ejecuta el análisis antes de enviar.")
    else:
        report_content = generate_report(st.session_state.eda_ok, st.session_state.df)
        ok = send_email(email_to, "Resultados del análisis", report_content)
        st.success("Correo enviado") if ok else st.error("Fallo al enviar. Revisa SMTP_* en variables de entorno.")

