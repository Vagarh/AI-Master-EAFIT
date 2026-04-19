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


# Límite de tamaño de archivo (25 MB)
MAX_FILE_SIZE = 25 * 1024 * 1024


def get_file_size(file) -> int:
    """Obtiene el tamaño del archivo en bytes."""
    if hasattr(file, "size"):
        # Objetos de Streamlit (UploadedFile)
        return file.size

    # Objetos file-like estándar (buscando hasta el final)
    current_pos = file.tell()
    file.seek(0, 2)  # Mover al final
    size = file.tell()
    file.seek(current_pos)  # Restaurar posición original
    return size


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

    # Validación de seguridad: Validar extensiones de archivo permitidas
    name = file.name.lower()
    allowed_extensions = [".csv", ".xls", ".xlsx"]
    if not any(name.endswith(ext) for ext in allowed_extensions):
        raise ValueError("Error de seguridad: Extensión de archivo no permitida. Solo se aceptan .csv, .xls, .xlsx")

    # Validación de seguridad: Prevenir DoS por archivos enormes
    file_size = get_file_size(file)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(f"Error de seguridad: El archivo excede el tamaño máximo permitido de 25MB.")

    # ============================================================
    # Procesamiento de archivos CSV
    # ============================================================
    if name.endswith(".csv"):
        try:
            # Validación de seguridad: Check por bytes nulos (indicador de archivo binario camuflado)
            raw_bytes = file.read(4096)
            if b'\x00' in raw_bytes:
                 raise ValueError("Error de seguridad: Se detectaron bytes nulos en el archivo CSV. Posible archivo binario malicioso.")

            # Leer una muestra del archivo para detectar el delimitador
            # Esto es útil para manejar tanto CSV separados por coma como por punto y coma
            raw = raw_bytes.decode(errors="ignore")
            dialect = csv.Sniffer().sniff(raw)
            delim = dialect.delimiter

        except ValueError as ve:
            # Re-lanzar excepciones de seguridad
            raise ve
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
