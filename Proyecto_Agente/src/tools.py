from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import io

import requests
def run_blast_search(sequence: str, top_n: int = 3):
    """
    Performs a BLAST search for a given protein sequence against the NCBI nr database
    and returns the top N results.

    Args:
        sequence (str): The protein sequence to search for.
        top_n (int): The number of top results to return.

    Returns:
        str: A formatted string with the top N BLAST results, or an error message.
    """
    if not sequence or not isinstance(sequence, str) or len(sequence) < 10:
        return "Error: Se necesita una secuencia de proteína válida (mínimo 10 aminoácidos) para la búsqueda BLAST."

    try:
        # Using io.StringIO to handle the result in memory
        result_handle = NCBIWWW.qblast("blastp", "nr", sequence)
        blast_records = NCBIXML.parse(result_handle)

        output = io.StringIO()
        output.write(f"Resultados de BLAST para la secuencia (primeros 50 AA): {sequence[:50]}...\n\n")
        
        count = 0
        for blast_record in blast_records:
            if not blast_record.alignments:
                return "No se encontraron alineaciones significativas para la secuencia proporcionada."
            
            for alignment in blast_record.alignments:
                if count >= top_n: break
                output.write(f"> {alignment.title}\n")
                for hsp in alignment.hsps:
                    output.write(f"  E-value: {hsp.expect:.2e} | Score: {hsp.score} | Identidades: {hsp.identities}/{hsp.align_length} ({ (hsp.identities / hsp.align_length) * 100 :.2f}%)\n")
                count += 1
            if count >= top_n: break
        
        return output.getvalue()

    except Exception as e:
        return f"Error al realizar la búsqueda BLAST: {e}"

def fetch_pdb_data(pdb_id: str):
    """
    Busca y devuelve metadatos para un ID de PDB específico desde la API de RCSB PDB.

    Args:
        pdb_id (str): El ID de 4 caracteres del Protein Data Bank (ej. '2HHB').

    Returns:
        str: Una cadena formateada con los metadatos de la entrada de PDB o un mensaje de error.
    """
    if not pdb_id or not isinstance(pdb_id, str) or len(pdb_id) != 4:
        return "Error: Se requiere un ID de PDB válido de 4 caracteres."

    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    try:
        response = requests.get(url)
        if response.status_code == 404:
            return f"Error: No se encontró ninguna entrada para el PDB ID '{pdb_id}'."
        response.raise_for_status()  # Lanza un error para otros códigos de estado HTTP malos

        data = response.json()
        
        # Extraer información clave
        title = data.get('struct', {}).get('title', 'No disponible')
        method = data.get('exptl', [{}])[0].get('method', 'No disponible')
        resolution = data.get('rcsb_entry_info', {}).get('resolution_combined', [None])[0]
        authors = ", ".join([author.get('name', '') for author in data.get('citation', [{}])[0].get('rcsb_authors', []) if author.get('name')])

        # Formatear la salida para el LLM
        output = (
            f"Resumen para PDB ID {pdb_id}:\n"
            f"- Título: {title}\n"
            f"- Método Experimental: {method}\n"
            f"- Resolución: {resolution:.2f} Å\n" if resolution else "- Resolución: No disponible\n"
            f"- Autores de la Publicación: {authors if authors else 'No disponibles'}"
        )
        return output

    except requests.exceptions.RequestException as e:
        return f"Error de red al contactar la API de PDB: {e}"
    except Exception as e:
        return f"Ocurrió un error inesperado al procesar los datos de PDB: {e}"
