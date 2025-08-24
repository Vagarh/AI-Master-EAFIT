import io
import streamlit as st

def generate_report(eda_ok, df):
    report = io.StringIO()
    report.write("# Resumen de análisis\n\n")
    report.write(f"- EDA disponible: {eda_ok}\n")
    if df is not None:
        report.write(f"- Shape: {df.shape}\n")
        num_cols = df.select_dtypes("number").columns.tolist()
        report.write(f"- Numéricas: {num_cols}\n")
    return report.getvalue()
