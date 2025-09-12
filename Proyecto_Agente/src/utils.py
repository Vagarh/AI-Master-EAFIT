"""
Utilidades generales para el Agente de Análisis de Proteínas
"""
import pandas as pd
import streamlit as st
from typing import Optional, Dict, Any
import re
from pathlib import Path

def validate_protein_sequence(sequence: str) -> Dict[str, Any]:
    """
    Valida una secuencia de proteína.
    
    Args:
        sequence: Secuencia de aminoácidos
        
    Returns:
        Diccionario con información de validación
    """
    # Aminoácidos estándar
    standard_aa = set('ACDEFGHIKLMNPQRSTVWY')
    
    # Limpiar secuencia
    clean_seq = sequence.upper().strip()
    
    # Validaciones
    validation = {
        "is_valid": True,
        "length": len(clean_seq),
        "has_invalid_chars": False,
        "invalid_chars": set(),
        "has_nonstd_aa": False,
        "nonstd_aa": set(),
        "composition": {}
    }
    
    # Verificar caracteres válidos
    seq_chars = set(clean_seq)
    invalid_chars = seq_chars - standard_aa - {'X', 'U', 'O', 'B', 'Z', 'J'}
    
    if invalid_chars:
        validation["has_invalid_chars"] = True
        validation["invalid_chars"] = invalid_chars
        validation["is_valid"] = False
    
    # Verificar aminoácidos no estándar
    nonstd_aa = seq_chars - standard_aa
    if nonstd_aa:
        validation["has_nonstd_aa"] = True
        validation["nonstd_aa"] = nonstd_aa
    
    # Composición de aminoácidos
    if clean_seq:
        for aa in standard_aa:
            count = clean_seq.count(aa)
            if count > 0:
                validation["composition"][aa] = {
                    "count": count,
                    "percentage": (count / len(clean_seq)) * 100
                }
    
    return validation

def format_sequence_display(sequence: str, line_length: int = 60) -> str:
    """
    Formatea una secuencia para mostrar en líneas de longitud específica.
    
    Args:
        sequence: Secuencia de aminoácidos
        line_length: Longitud de cada línea
        
    Returns:
        Secuencia formateada
    """
    lines = []
    for i in range(0, len(sequence), line_length):
        line = sequence[i:i+line_length]
        lines.append(f"{i+1:>6}: {line}")
    
    return "\n".join(lines)

def calculate_molecular_weight(sequence: str) -> float:
    """
    Calcula el peso molecular aproximado de una secuencia de proteína.
    
    Args:
        sequence: Secuencia de aminoácidos
        
    Returns:
        Peso molecular en Daltons
    """
    # Pesos moleculares de aminoácidos (Da)
    aa_weights = {
        'A': 89.09, 'R': 174.20, 'N': 132.12, 'D': 133.10, 'C': 121.15,
        'Q': 146.15, 'E': 147.13, 'G': 75.07, 'H': 155.16, 'I': 131.17,
        'L': 131.17, 'K': 146.19, 'M': 149.21, 'F': 165.19, 'P': 115.13,
        'S': 105.09, 'T': 119.12, 'W': 204.23, 'Y': 181.19, 'V': 117.15
    }
    
    weight = 0.0
    for aa in sequence.upper():
        weight += aa_weights.get(aa, 0.0)
    
    # Restar agua por cada enlace peptídico
    if len(sequence) > 1:
        weight -= (len(sequence) - 1) * 18.015
    
    return weight

def get_secondary_structure_info(sst3_sequence: str) -> Dict[str, Any]:
    """
    Analiza la secuencia de estructura secundaria.
    
    Args:
        sst3_sequence: Secuencia de estructura secundaria (H, E, C)
        
    Returns:
        Información sobre la estructura secundaria
    """
    if not sst3_sequence:
        return {}
    
    total_length = len(sst3_sequence)
    counts = {'H': 0, 'E': 0, 'C': 0}
    
    for char in sst3_sequence:
        if char in counts:
            counts[char] += 1
    
    structure_info = {
        'total_length': total_length,
        'helix_count': counts['H'],
        'sheet_count': counts['E'],
        'coil_count': counts['C'],
        'helix_percentage': (counts['H'] / total_length) * 100 if total_length > 0 else 0,
        'sheet_percentage': (counts['E'] / total_length) * 100 if total_length > 0 else 0,
        'coil_percentage': (counts['C'] / total_length) * 100 if total_length > 0 else 0,
        'dominant_structure': max(counts, key=counts.get) if any(counts.values()) else None
    }
    
    return structure_info

def create_download_link(data: bytes, filename: str, mime_type: str, label: str) -> str:
    """
    Crea un enlace de descarga para datos binarios.
    
    Args:
        data: Datos binarios
        filename: Nombre del archivo
        mime_type: Tipo MIME
        label: Etiqueta del enlace
        
    Returns:
        HTML del enlace de descarga
    """
    import base64
    
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}">{label}</a>'
    return href

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    División segura que evita división por cero.
    
    Args:
        numerator: Numerador
        denominator: Denominador
        default: Valor por defecto si el denominador es cero
        
    Returns:
        Resultado de la división o valor por defecto
    """
    return numerator / denominator if denominator != 0 else default

def format_large_number(number: int) -> str:
    """
    Formatea números grandes con separadores de miles.
    
    Args:
        number: Número a formatear
        
    Returns:
        Número formateado como string
    """
    return f"{number:,}"

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Trunca texto si excede la longitud máxima.
    
    Args:
        text: Texto a truncar
        max_length: Longitud máxima
        suffix: Sufijo a añadir si se trunca
        
    Returns:
        Texto truncado
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix

def extract_pdb_id(text: str) -> Optional[str]:
    """
    Extrae un ID de PDB de un texto.
    
    Args:
        text: Texto que puede contener un ID de PDB
        
    Returns:
        ID de PDB si se encuentra, None en caso contrario
    """
    # Patrón para ID de PDB (4 caracteres alfanuméricos)
    pattern = r'\b[1-9][A-Za-z0-9]{3}\b'
    match = re.search(pattern, text.upper())
    return match.group() if match else None

def create_progress_bar(current: int, total: int, label: str = "") -> None:
    """
    Crea una barra de progreso en Streamlit.
    
    Args:
        current: Valor actual
        total: Valor total
        label: Etiqueta opcional
    """
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"{label} {current}/{total} ({progress:.1%})")

class DataFrameValidator:
    """Validador para DataFrames de proteínas"""
    
    @staticmethod
    def validate_columns(df: pd.DataFrame, required_columns: set) -> Dict[str, Any]:
        """
        Valida que el DataFrame tenga las columnas requeridas.
        
        Args:
            df: DataFrame a validar
            required_columns: Conjunto de columnas requeridas
            
        Returns:
            Diccionario con información de validación
        """
        if df is None:
            return {"is_valid": False, "error": "DataFrame is None"}
        
        actual_columns = set(df.columns.str.lower())
        missing_columns = required_columns - actual_columns
        
        return {
            "is_valid": len(missing_columns) == 0,
            "missing_columns": missing_columns,
            "extra_columns": actual_columns - required_columns,
            "total_rows": len(df),
            "total_columns": len(df.columns)
        }
    
    @staticmethod
    def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Genera un reporte de calidad de datos.
        
        Args:
            df: DataFrame a analizar
            
        Returns:
            Reporte de calidad de datos
        """
        if df is None or df.empty:
            return {"error": "DataFrame is empty or None"}
        
        report = {
            "shape": df.shape,
            "null_counts": df.isnull().sum().to_dict(),
            "null_percentages": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "dtypes": df.dtypes.to_dict()
        }
        
        # Análisis específico para columnas de proteínas
        if 'len' in df.columns:
            report["length_stats"] = {
                "min": df['len'].min(),
                "max": df['len'].max(),
                "mean": df['len'].mean(),
                "median": df['len'].median(),
                "std": df['len'].std()
            }
        
        return report