from Bio.Blast import NCBIWWW
from Bio.Blast import NCBIXML
import io

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

