import streamlit as st
import pandas as pd
import eda
import agent

st.set_page_config(layout="wide")

st.title('Analizador de Secuencias de Proteínas con Agente IA')

st.write("""
Esta aplicación realiza un análisis exploratorio de datos (EDA) sobre un dataset de secuencias de proteínas
y permite interactuar con un agente de IA para obtener información sobre los datos.
""")

# Carga de datos
uploaded_file = st.sidebar.file_uploader("Cargar archivo CSV", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success("¡Archivo cargado exitosamente!")
        
        st.header("Análisis Exploratorio de Datos (EDA)")
        
        # Generar y mostrar EDA
        st.subheader("Estadísticas Descriptivas")
        st.dataframe(eda.get_descriptive_stats(df))
        
        st.subheader("Valores Nulos")
        st.dataframe(eda.get_null_values(df))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Distribución de Longitud de Secuencias")
            fig_len = eda.plot_length_histogram(df)
            st.pyplot(fig_len)
            
            st.subheader("Distribución de Estructuras Secundarias (Q3)")
            st.dataframe(eda.get_q3_distribution(df))

        with col2:
            st.subheader("Proporción de Aminoácidos no Estándar")
            fig_aa = eda.plot_nonstd_aa_proportion(df)
            st.pyplot(fig_aa)
            
            st.subheader("Distribución de Estructuras Secundarias (Q8)")
            st.dataframe(eda.get_q8_distribution(df))
        
        # --- Agente Interactivo con Herramientas ---
        st.header("Interactuar con el Agente de Biología v2.0")

        try:
            # Inicializar el agente y guardarlo en el estado de la sesión
            # El agente ahora necesita el dataframe para sus herramientas de EDA
            if 'agent_executor' not in st.session_state:
                with st.spinner("Inicializando agente con herramientas... Por favor, espera."):
                    st.session_state.agent_executor = agent.create_tool_agent(df)
            
            user_question = st.text_input("Haz una pregunta o pide una visualización (ej: 'Busca hemoglobina' o 'Genera el histograma de longitud')")

            if user_question:
                with st.spinner("El agente está pensando y usando sus herramientas..."):
                    response = st.session_state.agent_executor.invoke({
                        "input": user_question
                    })
                    
                    # La respuesta del agente es un diccionario, la respuesta final está en la clave 'output'
                    output_text = response.get("output", "No se pudo obtener una respuesta.")
                    st.markdown(output_text)

                    # Si el agente generó un gráfico, lo mostramos
                    if "Histograma de longitud generado" in output_text:
                        # Extraemos la ruta del archivo de la respuesta del agente
                        filepath = output_text.split(": ")[-1]
                        if os.path.exists(filepath):
                            st.image(filepath)
                        else:
                            st.error("El agente dijo que creó un gráfico, pero no se encontró el archivo.")

        except ValueError as e:
            st.error(f"Error al inicializar el agente: {e}")
        except Exception as e:
            st.error(f"Ocurrió un error inesperado con el agente: {e}")

    except Exception as e:
        st.sidebar.error(f"Error al procesar el archivo: {e}")
else:
    st.info("Por favor, carga un archivo CSV para comenzar el análisis.")