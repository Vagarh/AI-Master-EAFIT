import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def validate_eda(df):
    if df is None:
        return False
    needed_cols = {"seq", "sst3", "sst8", "len", "has_nonstd_aa"}
    actual_cols = {c.lower() for c in df.columns}
    return needed_cols.issubset(actual_cols)

# ------------------------------
# Análisis de secuencias
# ------------------------------

def plot_length_distribution(df):
    """Histograma de la distribución de longitudes de secuencia."""
    fig, ax = plt.subplots()
    sns.histplot(df['len'], kde=True, ax=ax, bins=30, color="steelblue")
    ax.set_title('Distribución de la Longitud de las Secuencias')
    ax.set_xlabel('Longitud')
    ax.set_ylabel('Frecuencia')
    return fig

def plot_q3_distribution(df):
    """Gráfico de barras de la frecuencia de estructuras secundarias (Q3)."""
    q3_counts = pd.Series(list("".join(df['sst3']))).value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=q3_counts.index, y=q3_counts.values, ax=ax, palette="viridis")
    ax.set_title('Frecuencia de Estructuras Secundarias (Q3)')
    ax.set_xlabel('Tipo de Estructura (H: Hélice, E: Hoja, C: Coil)')
    ax.set_ylabel('Conteo Total')
    return fig

def plot_nonstd_aa_pie(df):
    """Proporción de secuencias con aminoácidos no estándar."""
    counts = df['has_nonstd_aa'].value_counts()
    labels = {True: 'Con Aminoácidos No Estándar', False: 'Solo Estándar'}
    fig, ax = plt.subplots()
    ax.pie(counts, labels=[labels[i] for i in counts.index], 
           autopct='%1.1f%%', startangle=90, colors=sns.color_palette("pastel"))
    ax.set_title('Proporción de Secuencias con Aminoácidos No Estándar')
    ax.axis('equal')
    return fig

# ------------------------------
# Análisis de calidad estructural
# ------------------------------

def plot_resolution_distribution(df):
    """Distribución de la resolución estructural."""
    fig, ax = plt.subplots()
    sns.histplot(df['resolution'], kde=True, bins=30, ax=ax, color="darkorange")
    ax.set_title('Distribución de Resoluciones de las Estructuras')
    ax.set_xlabel('Resolución (Å)')
    ax.set_ylabel('Frecuencia')
    return fig

def plot_rfactor_distribution(df):
    """Distribución del R-factor experimental."""
    fig, ax = plt.subplots()
    sns.histplot(df['R-factor'], kde=True, bins=30, ax=ax, color="teal")
    ax.set_title('Distribución del R-factor')
    ax.set_xlabel('R-factor')
    ax.set_ylabel('Frecuencia')
    return fig

def plot_experimental_methods(df):
    """Conteo de estructuras por método experimental."""
    fig, ax = plt.subplots()
    sns.countplot(x='Exptl.', data=df, ax=ax, palette="Set2")
    ax.set_title('Métodos Experimentales en el Dataset')
    ax.set_xlabel('Método Experimental')
    ax.set_ylabel('Número de Estructuras')
    return fig

def plot_length_vs_resolution(df):
    """Relación entre la longitud de la secuencia y la resolución experimental."""
    fig, ax = plt.subplots()
    sns.scatterplot(x='len', y='resolution', data=df, alpha=0.5, ax=ax, color="purple")
    ax.set_title('Longitud de Secuencia vs Resolución Experimental')
    ax.set_xlabel('Longitud de Secuencia')
    ax.set_ylabel('Resolución (Å)')
    return fig

