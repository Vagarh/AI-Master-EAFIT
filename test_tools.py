import sys
from unittest.mock import MagicMock
sys.modules['requests'] = MagicMock()
sys.modules['Bio'] = MagicMock()
sys.modules['Bio.Blast'] = MagicMock()

import unittest
from Proyecto_Agente.src.tools import run_blast_search, fetch_pdb_data

class TestToolsValidation(unittest.TestCase):
    def test_fetch_pdb_data_validation(self):
        # Longitud incorrecta
        self.assertIn("Error", fetch_pdb_data("2HH"))
        self.assertIn("Error", fetch_pdb_data("2HHBA"))

        # Formato incorrecto (no empieza con número 1-9)
        self.assertIn("Error: El ID de PDB", fetch_pdb_data("0HHB"))
        self.assertIn("Error: El ID de PDB", fetch_pdb_data("AHHB"))

        # Caracteres especiales
        self.assertIn("Error: El ID de PDB", fetch_pdb_data("2H-B"))

    def test_run_blast_search_validation(self):
        # Longitud menor a 10
        self.assertIn("mínimo 10 aminoácidos", run_blast_search("ACDEF"))

        # Caracteres no alfabéticos ni *
        self.assertIn("caracteres inválidos", run_blast_search("ACDEFGHIK123"))
        self.assertIn("caracteres inválidos", run_blast_search("ACDEFGHIKL-MN"))

if __name__ == '__main__':
    unittest.main()
