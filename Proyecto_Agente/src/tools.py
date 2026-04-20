"""
Herramientas bioinformáticas para el Agente de Análisis de Proteínas.

Este módulo proporciona funciones para interactuar con bases de datos bioinformáticas
externas como NCBI BLAST y RCSB Protein Data Bank (PDB). Estas herramientas permiten
al agente obtener información adicional sobre secuencias y estructuras de proteínas.

Author: Juan Felipe Cardona
Date: 2024
"""

import io
import re
from typing import Optional
import requests
from Bio.Blast import NCBIWWW, NCBIXML


def run_blast_search(sequence: str, top_n: int = 3) -> str:
    """
    Realiza una búsqueda BLAST para una secuencia de proteína dada contra la base de datos nr de NCBI.

    Esta función permite encontrar secuencias similares en la base de datos no redundante
    de NCBI, útil para identificar proteínas homólogas o relacionadas evolutivamente.

    Args:
        sequence (str): Secuencia de aminoácidos a buscar. Debe contener al menos 10 residuos.
        top_n (int, optional): Número de mejores resultados a retornar. Por defecto 3.

    Returns:
        str: String formateado con los top N resultados BLAST incluyendo:
             - Título de la secuencia encontrada
             - E-value (significancia estadística)
             - Score de alineamiento
             - Porcentaje de identidad

    Raises:
        Exception: Si ocurre un error durante la búsqueda BLAST

    Example:
        >>> sequence = "MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNL..."
        >>> results = run_blast_search(sequence, top_n=5)
    """
    # ============================================================
    # Validación de entrada
    # ============================================================
    if not sequence or not isinstance(sequence, str) or len(sequence) < 10:
        return "Error: Se necesita una secuencia de proteína válida (mínimo 10 aminoácidos) para la búsqueda BLAST."

    # Validación de seguridad estricta para evitar Inyección en APIs externas
    # Permitir letras (aminoácidos) y asterisco (codón de parada)
    if not re.match(r'^[A-Za-z\*]+$', sequence):
        return "Error: La secuencia contiene caracteres inválidos. Solo se permiten letras (A-Z) y asteriscos (*)."

    try:
        # ============================================================
        # Ejecutar búsqueda BLAST remota
        # ============================================================
        # Nota: qblast realiza la búsqueda en los servidores de NCBI
        # blastp = búsqueda de proteína vs proteína
        # nr = base de datos no redundante
        result_handle = NCBIWWW.qblast("blastp", "nr", sequence)
        blast_records = NCBIXML.parse(result_handle)

        # Buffer para construir la salida formateada
        output = io.StringIO()
        output.write(f"Resultados de BLAST para la secuencia (primeros 50 AA): {sequence[:50]}...\n\n")

        # ============================================================
        # Procesar y formatear resultados
        # ============================================================
        count = 0
        for blast_record in blast_records:
            # Verificar si se encontraron alineamientos
            if not blast_record.alignments:
                return "No se encontraron alineaciones significativas para la secuencia proporcionada."

            # Iterar sobre los alineamientos encontrados
            for alignment in blast_record.alignments:
                if count >= top_n:
                    break

                # Escribir información del hit
                output.write(f"> {alignment.title}\n")

                # Procesar HSPs (High-scoring Segment Pairs)
                for hsp in alignment.hsps:
                    identity_pct = (hsp.identities / hsp.align_length) * 100
                    output.write(
                        f"  E-value: {hsp.expect:.2e} | "
                        f"Score: {hsp.score} | "
                        f"Identidades: {hsp.identities}/{hsp.align_length} ({identity_pct:.2f}%)\n"
                    )

                count += 1

            if count >= top_n:
                break

        return output.getvalue()

    except Exception as e:
        return f"Error al realizar la búsqueda BLAST: {e}"

def fetch_pdb_data(pdb_id: str) -> str:
    """
    Obtiene metadatos de una estructura cristalográfica desde la base de datos RCSB PDB.

    Consulta la API REST de RCSB para recuperar información detallada sobre
    una estructura de proteína, incluyendo título, método experimental,
    resolución y autores.

    Args:
        pdb_id (str): Identificador de 4 caracteres del PDB (ej. '2HHB' para hemoglobina).

    Returns:
        str: Información formateada sobre la estructura que incluye:
             - Título de la estructura
             - Método experimental utilizado
             - Resolución de la estructura (si aplica)
             - Autores de la publicación

    Raises:
        requests.exceptions.RequestException: Si hay problemas de conexión con la API

    Example:
        >>> info = fetch_pdb_data("2HHB")
        >>> print(info)
        Resumen para PDB ID 2HHB:
        - Título: DEOXY HUMAN HEMOGLOBIN
        - Método Experimental: X-RAY DIFFRACTION
        - Resolución: 1.74 Å
    """
    # ============================================================
    # Validación de entrada
    # ============================================================
    if not pdb_id or not isinstance(pdb_id, str) or len(pdb_id) != 4:
        return "Error: Se requiere un ID de PDB válido de 4 caracteres."

    # Validación de seguridad estricta para evitar SSRF/Injection
    # PDB IDs son estrictamente 4 caracteres (1 número + 3 alfanuméricos)
    if not re.match(r'^[1-9][a-zA-Z0-9]{3}$', pdb_id):
        return "Error: El ID de PDB contiene caracteres no válidos o no tiene el formato correcto."

    # ============================================================
    # Consultar API de RCSB PDB
    # ============================================================
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"

    try:
        # Realizar petición GET a la API
        # Validación de seguridad: Timeout explícito para evitar bloqueos
        response = requests.get(url, timeout=10)

        # Verificar si el PDB ID existe
        if response.status_code == 404:
            return f"Error: No se encontró ninguna entrada para el PDB ID '{pdb_id}'."

        # Lanzar excepción si hay otros errores HTTP
        response.raise_for_status()

        # Parsear respuesta JSON
        data = response.json()

        # ============================================================
        # Extraer información relevante
        # ============================================================
        title = data.get('struct', {}).get('title', 'No disponible')
        method = data.get('exptl', [{}])[0].get('method', 'No disponible')
        resolution = data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0]

        # Extraer autores de la publicación asociada
        authors = ", ".join([
            author.get('name', '')
            for author in data.get('citation', [{}])[0].get('rcsb_authors', [])
            if author.get('name')
        ])

        # ============================================================
        # Formatear salida para el LLM
        # ============================================================
        output = (
            f"Resumen para PDB ID {pdb_id}:\n"
            f"- Título: {title}\n"
            f"- Método Experimental: {method}\n"
        )

        # Añadir resolución si está disponible
        if resolution:
            output += f"- Resolución: {resolution:.2f} Å\n"
        else:
            output += "- Resolución: No disponible\n"

        # Añadir autores
        output += f"- Autores de la Publicación: {authors if authors else 'No disponibles'}"

        return output

    except requests.exceptions.RequestException as e:
        return f"Error de red al contactar la API de PDB: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado al procesar los datos de PDB: {e}"
