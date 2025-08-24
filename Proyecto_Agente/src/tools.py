from langchain.tools import tool
from default_api import google_web_search
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from src.eda import get_amino_acid_composition, get_hydrophobicity_scores, get_q3_distribution, get_q8_distribution

@tool
def biological_web_search(query: str) -> str:
    """Busca información sobre conceptos biológicos o biomédicos en Google.
    Útil cuando se necesita información actualizada o no disponible en el contexto.
    Ejemplo de entrada: 'función de la ATP sintasa' o 'qué es la PCR'."""
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

@tool
def analyze_amino_acid_composition(dataframe: pd.DataFrame) -> str:
 """
 Calcula y devuelve la composición de aminoácidos (conteo y frecuencia) del dataset.
 Es útil para entender la abundancia relativa de cada aminoácido.
 La entrada debe ser el DataFrame de pandas completo.
 """
    print("Analizando composición de aminoácidos...")
    composition_df = get_amino_acid_composition(dataframe)
 return composition_df.to_string()

@tool
def analyze_hydrophobicity(dataframe: pd.DataFrame) -> str:
 """
 Calcula y devuelve estadísticas descriptivas de los scores promedio de hidrofobicidad por secuencia.
 Utiliza la escala de Kyte-Doolittle. Útil para entender la tendencia de hidrofobicidad general del dataset.
 La entrada debe ser el DataFrame de pandas completo.
 """
 print("Analizando scores de hidrofobicidad...")
    hydro_scores = get_hydrophobicity_scores(dataframe)
 return hydro_scores.describe().to_string()

@tool
def analyze_secondary_structure_q3(dataframe: pd.DataFrame) -> str:
 """Devuelve la distribución de los estados secundarios Q3 (3 clases)."""
 return get_q3_distribution(dataframe).to_string()

@tool
def analyze_secondary_structure_q8(dataframe: pd.DataFrame) -> str:
 """Devuelve la distribución de los estados secundarios Q8 (8 clases)."""
 return get_q8_distribution(dataframe).to_string()
