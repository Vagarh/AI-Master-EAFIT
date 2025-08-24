import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def validate_eda(df):
    if df is None:
        return False
    needed_cols = {"seq", "sst3", "sst8", "len", "has_nonstd_aa"}
    actual_cols = {c.lower() for c in df.columns}
    return needed_cols.issubset(actual_cols)

def plot_length_distribution(df):
    """Genera un histograma de la distribución de longitudes de secuencia."""
    fig, ax = plt.subplots()
    sns.histplot(df['len'], kde=True, ax=ax, bins=30)
    ax.set_title('Distribución de la Longitud de las Secuencias')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Frecuencia')
    return fig

def plot_q3_distribution(df):
    """Genera un gráfico de barras de la frecuencia de estructuras secundarias (Q3)."""
    # Contar cada tipo de estructura en la columna 'sst3'
    q3_counts = pd.Series(list("".join(df['sst3']))).value_counts()
    
    fig, ax = plt.subplots()
    sns.barplot(x=q3_counts.index, y=q3_counts.values, ax=ax, palette="viridis")
    ax.set_title('Frecuencia de Estructuras Secundarias (Q3)')
    ax.set_xlabel('Tipo de Estructura (H: Hélice, E: Hoja, C: Espiral)')
    ax.set_ylabel('Conteo Total')
    return fig

def plot_nonstd_aa_pie(df):
    """Genera un gráfico de torta mostrando la proporción de secuencias con aminoácidos no estándar."""
    counts = df['has_nonstd_aa'].value_counts()
    labels = {True: 'Con Aminoácidos No Estándar', False: 'Solo Estándar'}
    
    fig, ax = plt.subplots()
    ax.pie(counts, labels=[labels[i] for i in counts.index], autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title('Proporción de Secuencias con Aminoácidos No Estándar')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    return fig
