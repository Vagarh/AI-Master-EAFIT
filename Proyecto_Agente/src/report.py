import io
import streamlit as st
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt

# Importar las funciones de ploteo para usarlas en el reporte
from eda import plot_length_distribution, plot_q3_distribution, plot_nonstd_aa_pie

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

class PDF(FPDF):
    """Clase extendida para crear cabecera y pie de página."""
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Informe de Análisis de Proteínas', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 6, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Courier', '', 9)
        self.multi_cell(0, 5, body)
        self.ln()
        self.set_font('Arial', '', 12)

    def add_plot(self, fig, title):
        self.add_page()
        self.chapter_title(title)
        with io.BytesIO() as buffer:
            fig.savefig(buffer, format="png", bbox_inches='tight')
            # Ancho de página A4 es 210mm, dejamos márgenes
            self.image(buffer, w=190)
        plt.close(fig) # Cerramos la figura para liberar memoria

def generate_pdf_report(eda_ok, df):
    """Genera un reporte completo en formato PDF con textos y gráficos."""
    if not eda_ok or df is None:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Error: No se pudo generar el reporte.', 0, 1, 'C')
        return bytes(pdf.output())

    pdf = PDF()
    pdf.add_page()

    # Metadata y fecha
    pdf.set_title("Reporte de Análisis de Proteínas")
    pdf.set_author("Agente de Análisis")
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 10, f"Fecha de generación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1, 'R')

    # Contenido del reporte
    pdf.chapter_title("1. Resumen General")
    pdf.chapter_body(f"- Filas: {df.shape[0]}\n- Columnas: {df.shape[1]}")

    pdf.chapter_title("2. Vista Previa de los Datos")
    pdf.chapter_body(df.head(10).to_string())

    pdf.chapter_title("3. Resumen de Valores Nulos")
    pdf.chapter_body(df.isna().sum().to_frame("nulos").to_string())

    pdf.chapter_title("4. Estadísticas Descriptivas")
    pdf.chapter_body(df.select_dtypes("number").describe().T.to_string())

    # Añadir gráficos
    fig_len = plot_length_distribution(df)
    pdf.add_plot(fig_len, "5. Distribución de la Longitud de las Secuencias")

    fig_q3 = plot_q3_distribution(df)
    pdf.add_plot(fig_q3, "6. Frecuencia de Estructuras Secundarias (Q3)")

    fig_pie = plot_nonstd_aa_pie(df)
    pdf.add_plot(fig_pie, "7. Proporción de Aminoácidos No Estándar")

    return bytes(pdf.output())
