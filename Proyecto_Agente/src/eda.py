import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from collections import Counter

def get_descriptive_stats(df):
    """Devuelve estadísticas descriptivas del DataFrame."""
    return df.describe()

def get_null_values(df):
    """Devuelve la cuenta de valores nulos por columna."""
    return df.isnull().sum()

def plot_length_histogram(df):
    """Genera un histograma de la longitud de las secuencias."""
    fig, ax = plt.subplots()
    sns.histplot(df['len'], kde=True, ax=ax)
    ax.set_title('Distribución de la Longitud de las Secuencias')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Frecuencia')
    return fig

def get_q3_distribution(df):
    """Devuelve la distribución de los estados secundarios Q3."""
    return df['sst3'].value_counts()

def get_q8_distribution(df):
    """Devuelve la distribución de los estados secundarios Q8."""
    return df['sst8'].value_counts()

def plot_nonstd_aa_proportion(df):
    """Genera un gráfico de pastel de la proporción de aminoácidos no estándar."""
    fig, ax = plt.subplots()
    df['has_nonstd_aa'].value_counts().plot.pie(autopct='%1.1f%%', ax=ax)
    ax.set_title('Proporción de Secuencias con Aminoácidos no Estándar')
    ax.set_ylabel('')
    return fig

def get_amino_acid_composition(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula y devuelve la composición de aminoácidos de las secuencias.
    Retorna un DataFrame con el conteo y la frecuencia de cada aminoácido.
    """
    all_amino_acids = "".join(df['sequence'].dropna())
    aa_counts = Counter(all_amino_acids)
    total_aas = sum(aa_counts.values())
    aa_frequencies = {aa: count / total_aas for aa, count in aa_counts.items()}

    composition_df = pd.DataFrame({
        'count': pd.Series(aa_counts),
        'frequency': pd.Series(aa_frequencies)
    }).sort_index()

    return composition_df

def get_hydrophobicity_scores(df: pd.DataFrame) -> pd.Series:
    """
    Calcula y devuelve el score promedio de hidrofobicidad para cada secuencia.
    Utiliza la escala de Kyte-Doolittle.
    """
    kyte_doolittle = {'A': 1.8, 'R': -4.5, 'N': -3.5, 'D': -3.5, 'C': 2.5,
                      'Q': -3.5, 'E': -3.5, 'G': -0.4, 'H': -3.2, 'I': 4.5,
                      'L': 3.8, 'K': -3.9, 'M': 1.9, 'F': 2.8, 'P': -1.6,
                      'S': -0.8, 'T': -0.7, 'W': -0.9, 'Y': -1.3, 'V': 4.2}

    # Handle potential non-standard amino acids by assigning a neutral score or skipping
    hydro_scores = df['sequence'].apply(lambda seq: sum(kyte_doolittle.get(aa, 0) for aa in seq) / len(seq) if len(seq) > 0 else 0)
    return hydro_scores

def generate_eda_summary(df):
    """Genera un resumen de texto del EDA para el agente LLM."""
    buffer = io.StringIO()
    
    buffer.write("Resumen del Análisis Exploratorio de Datos (EDA):\n\n")
    
    buffer.write("1. Estadísticas Descriptivas:\n")
    buffer.write(get_descriptive_stats(df).to_string())
    buffer.write("\n\n")
    
    buffer.write("2. Valores Nulos por Columna:\n")
    buffer.write(get_null_values(df).to_string())
    buffer.write("\n\n")
    
    buffer.write("3. Distribución de Estructuras Secundarias (Q3):\n")
    buffer.write(get_q3_distribution(df).to_string())
    buffer.write("\n\n")
    
    buffer.write("4. Distribución de Estructuras Secundarias (Q8):\n")
    buffer.write(get_q8_distribution(df).to_string())
    buffer.write("\n\n")
    
    buffer.write("5. Proporción de Aminoácidos no Estándar:\n")
    buffer.write(df['has_nonstd_aa'].value_counts(normalize=True).to_string())
    buffer.write("\n")

    buffer.write("6. Composición de Aminoácidos:\\n")
    buffer.write(get_amino_acid_composition(df).to_string())
    buffer.write("\\n\\n")

    buffer.write("7. Scores Promedio de Hidrofobicidad:\\n")
    buffer.write(get_hydrophobicity_scores(df).describe().to_string()) # Describe the series for summary
    buffer.write("\\n")
    
    return buffer.getvalue()