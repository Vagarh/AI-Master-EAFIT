from langchain.tools import tool
from default_api import google_web_search
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

@tool
def search_protein_info(query: str) -> str:
    """Busca información sobre una proteína o concepto biológico en Google.
    Útil cuando se necesita información actualizada o no disponible en el contexto.
    Ejemplo de entrada: 'hemoglobina' o 'estructura alfa-hélice'."""
    print(f"Buscando en la web: {query}")
    return google_web_search(query=query)

@tool
def generate_length_histogram(dataframe: pd.DataFrame) -> str:
    """Genera un histograma de la longitud de las secuencias de proteínas y devuelve la ruta del archivo de imagen.
    Es útil para visualizar la distribución de las longitudes de las secuencias en el dataset.
    La entrada debe ser el DataFrame de pandas completo."""
    print("Generando histograma de longitud...")
    fig, ax = plt.subplots()
    sns.histplot(dataframe['len'], kde=True, ax=ax)
    ax.set_title('Distribución de la Longitud de las Secuencias')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Frecuencia')
    
    # Guardar la figura en un archivo temporal
    if not os.path.exists("temp_charts"):
        os.makedirs("temp_charts")
        
    filepath = "temp_charts/length_histogram.png"
    fig.savefig(filepath)
    plt.close(fig)
    
    print(f"Histograma guardado en: {filepath}")
    return f"Histograma de longitud generado y guardado en: {filepath}"

# Podríamos añadir más herramientas para otros gráficos aquí
# Por ejemplo: generate_q3_distribution_chart, etc.
