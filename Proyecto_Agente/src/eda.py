"""
Módulo de Análisis Exploratorio de Datos (EDA) para datasets de proteínas.

Este módulo proporciona funciones para validar y visualizar datos de secuencias
de proteínas, incluyendo distribuciones de longitudes, estructuras secundarias,
calidad de datos y métricas experimentales.

Author: Juan Felipe Cardona
Date: 2024
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import Optional
from matplotlib.figure import Figure


def validate_eda(df: Optional[pd.DataFrame]) -> bool:
    """
    Valida que un DataFrame contenga las columnas mínimas requeridas para el análisis EDA.

    Args:
        df (pd.DataFrame): DataFrame a validar

    Returns:
        bool: True si el DataFrame contiene todas las columnas requeridas, False en caso contrario

    Example:
        >>> df = pd.read_csv("protein_data.csv")
        >>> is_valid = validate_eda(df)
    """
    if df is None:
        return False

    # Columnas requeridas para el análisis básico
    needed_cols = {"seq", "sst3", "sst8", "len", "has_nonstd_aa"}
    actual_cols = {c.lower() for c in df.columns}

    return needed_cols.issubset(actual_cols)


# ============================================================
# ANÁLISIS DE SECUENCIAS
# ============================================================

def plot_length_distribution(df: pd.DataFrame) -> Figure:
    """
    Genera un histograma de la distribución de longitudes de secuencias.

    Visualiza cómo se distribuyen las longitudes de las secuencias de proteínas
    en el dataset, incluyendo una estimación de densidad de kernel (KDE).

    Args:
        df (pd.DataFrame): DataFrame con columna 'len' (longitud de secuencias)

    Returns:
        Figure: Objeto matplotlib Figure con el histograma generado
    """
    fig, ax = plt.subplots()
    sns.histplot(df['len'], kde=True, ax=ax, bins=30, color="steelblue")
    ax.set_title('Distribución de la Longitud de las Secuencias')
    ax.set_xlabel('Longitud (aminoácidos)')
    ax.set_ylabel('Frecuencia')
    return fig


def plot_q3_distribution(df: pd.DataFrame) -> Figure:
    """
    Gráfico de barras de la frecuencia de estructuras secundarias (Q3).

    Muestra la distribución de los tres tipos principales de estructura secundaria:
    H (Hélice alfa), E (Hoja beta), C (Coil/Loop).

    Args:
        df (pd.DataFrame): DataFrame con columna 'sst3' (estructura secundaria en 3 estados)

    Returns:
        Figure: Objeto matplotlib Figure con el gráfico de barras
    """
    # Concatenar todas las secuencias de estructura secundaria y contar
    q3_counts = pd.Series(list("".join(df['sst3']))).value_counts()

    fig, ax = plt.subplots()
    sns.barplot(x=q3_counts.index, y=q3_counts.values, ax=ax, palette="viridis")
    ax.set_title('Frecuencia de Estructuras Secundarias (Q3)')
    ax.set_xlabel('Tipo de Estructura (H: Hélice, E: Hoja, C: Coil)')
    ax.set_ylabel('Conteo Total')
    return fig


def plot_nonstd_aa_pie(df: pd.DataFrame) -> Figure:
    """
    Gráfico circular de proporción de secuencias con aminoácidos no estándar.

    Visualiza qué porcentaje del dataset contiene secuencias con aminoácidos
    no estándar (X, U, O, B, Z, J) vs. solo aminoácidos estándar.

    Args:
        df (pd.DataFrame): DataFrame con columna 'has_nonstd_aa' (booleano)

    Returns:
        Figure: Objeto matplotlib Figure con el gráfico circular
    """
    counts = df['has_nonstd_aa'].value_counts()
    labels = {True: 'Con Aminoácidos No Estándar', False: 'Solo Estándar'}

    fig, ax = plt.subplots()
    ax.pie(
        counts,
        labels=[labels[i] for i in counts.index],
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("pastel")
    )
    ax.set_title('Proporción de Secuencias con Aminoácidos No Estándar')
    ax.axis('equal')  # Para que el gráfico sea circular
    return fig


# ============================================================
# ANÁLISIS DE CALIDAD ESTRUCTURAL
# ============================================================

def plot_resolution_distribution(df: pd.DataFrame) -> Figure:
    """
    Histograma de la distribución de resoluciones de estructuras cristalográficas.

    La resolución (medida en Ångströms) indica la calidad de los datos
    cristalográficos. Valores más bajos = mayor resolución/calidad.

    Args:
        df (pd.DataFrame): DataFrame con columna 'resolution'

    Returns:
        Figure: Objeto matplotlib Figure con el histograma
    """
    fig, ax = plt.subplots()
    sns.histplot(df['resolution'], kde=True, bins=30, ax=ax, color="darkorange")
    ax.set_title('Distribución de Resoluciones de las Estructuras')
    ax.set_xlabel('Resolución (Å)')
    ax.set_ylabel('Frecuencia')
    return fig


def plot_rfactor_distribution(df: pd.DataFrame) -> Figure:
    """
    Histograma de la distribución del R-factor experimental.

    El R-factor es una medida de la calidad del modelo cristalográfico.
    Valores típicos están entre 0.15-0.25 para estructuras de buena calidad.

    Args:
        df (pd.DataFrame): DataFrame con columna 'R-factor'

    Returns:
        Figure: Objeto matplotlib Figure con el histograma
    """
    fig, ax = plt.subplots()
    sns.histplot(df['R-factor'], kde=True, bins=30, ax=ax, color="teal")
    ax.set_title('Distribución del R-factor')
    ax.set_xlabel('R-factor')
    ax.set_ylabel('Frecuencia')
    return fig


def plot_experimental_methods(df: pd.DataFrame) -> Figure:
    """
    Gráfico de barras con el conteo de estructuras por método experimental.

    Muestra la distribución de métodos utilizados para determinar las estructuras
    (ej. X-RAY DIFFRACTION, NMR, ELECTRON MICROSCOPY).

    Args:
        df (pd.DataFrame): DataFrame con columna 'Exptl.' (método experimental)

    Returns:
        Figure: Objeto matplotlib Figure con el gráfico de barras
    """
    fig, ax = plt.subplots()
    sns.countplot(x='Exptl.', data=df, ax=ax, palette="Set2")
    ax.set_title('Métodos Experimentales en el Dataset')
    ax.set_xlabel('Método Experimental')
    ax.set_ylabel('Número de Estructuras')
    return fig


def plot_length_vs_resolution(df: pd.DataFrame) -> Figure:
    """
    Scatter plot de la relación entre longitud de secuencia y resolución.

    Explora si existe una correlación entre el tamaño de la proteína
    y la resolución cristalográfica obtenida.

    Args:
        df (pd.DataFrame): DataFrame con columnas 'len' y 'resolution'

    Returns:
        Figure: Objeto matplotlib Figure con el scatter plot
    """
    fig, ax = plt.subplots()
    sns.scatterplot(x='len', y='resolution', data=df, alpha=0.5, ax=ax, color="purple")
    ax.set_title('Longitud de Secuencia vs Resolución Experimental')
    ax.set_xlabel('Longitud de Secuencia (aminoácidos)')
    ax.set_ylabel('Resolución (Å)')
    return fig

