import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

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
    
    return buffer.getvalue()