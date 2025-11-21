"""
Utilidades de entrada/salida (I/O) para manejo de archivos.

Este módulo proporciona funciones para leer archivos de diferentes formatos
(CSV, Excel) de manera robusta, con detección automática de delimitadores.

Author: Juan Felipe Cardona
Date: 2024
"""

import pandas as pd
import csv
from typing import Optional


def read_any(file) -> Optional[pd.DataFrame]:
    """
    Lee archivos de datos en múltiples formatos (CSV, XLS, XLSX) con detección automática.

    Esta función detecta automáticamente el delimitador en archivos CSV y
    maneja tanto archivos CSV como Excel de manera transparente.

    Args:
        file: Objeto archivo subido (típicamente desde Streamlit file_uploader).
              Debe tener atributos 'name' para el nombre del archivo.

    Returns:
        pd.DataFrame: DataFrame con los datos cargados, o None si el archivo es inválido

    Raises:
        Exception: Si ocurre un error al leer el archivo

    Example:
        >>> uploaded_file = st.file_uploader("Sube tu archivo")
        >>> df = read_any(uploaded_file)
    """
    # Validar entrada
    if file is None:
        return None

    # Obtener nombre del archivo en minúsculas para comparación
    name = file.name.lower()

    # ============================================================
    # Procesamiento de archivos CSV
    # ============================================================
    if name.endswith(".csv"):
        try:
            # Leer una muestra del archivo para detectar el delimitador
            # Esto es útil para manejar tanto CSV separados por coma como por punto y coma
            raw = file.read(4096).decode(errors="ignore")
            dialect = csv.Sniffer().sniff(raw)
            delim = dialect.delimiter

        except Exception:
            # Si falla la detección, usar coma por defecto
            delim = ","

        finally:
            # Resetear el puntero del archivo al inicio para la lectura completa
            file.seek(0)

        # Leer el CSV completo con el delimitador detectado
        return pd.read_csv(file, delimiter=delim)

    # ============================================================
    # Procesamiento de archivos Excel (.xls, .xlsx)
    # ============================================================
    else:
        return pd.read_excel(file)
