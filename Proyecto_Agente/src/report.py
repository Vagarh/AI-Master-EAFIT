import io
import streamlit as st

def generate_report(eda_ok, df):
    """
    Genera un informe de texto completo del Análisis Exploratorio de Datos (EDA).
    """
    report = io.StringIO()
    report.write("========================================\n")
    report.write("  INFORME DE ANÁLISIS EXPLORATORIO (EDA)\n")
    report.write("========================================\n\n")

    if not eda_ok or df is None:
        report.write("El análisis no se pudo completar o el dataset no es válido.\n")
        report.write(f"Validación de EDA superada: {eda_ok}\n")
        return report.getvalue()

    # 1. Resumen General
    report.write("### 1. Resumen General ###\n")
    report.write(f"- Filas: {df.shape[0]}\n")
    report.write(f"- Columnas: {df.shape[1]}\n\n")

    # 2. Vista Previa de los Datos (Primeras 20 filas)
    report.write("### 2. Vista Previa de los Datos ###\n")
    report.write("Mostrando las primeras 20 filas del dataset:\n")
    report.write(df.head(20).to_string())
    report.write("\n\n")

    # 3. Resumen de Valores Nulos
    report.write("### 3. Resumen de Valores Nulos por Columna ###\n")
    report.write(df.isna().sum().to_frame("nulos").to_string())
    report.write("\n\n")

    # 4. Estadísticas Descriptivas para Columnas Numéricas
    report.write("### 4. Estadísticas Descriptivas (Columnas Numéricas) ###\n")
    report.write(df.select_dtypes("number").describe().T.to_string())
    report.write("\n")

    return report.getvalue()
