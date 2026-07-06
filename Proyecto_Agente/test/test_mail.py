import unittest
import os
from unittest.mock import patch
from src.mail import send_email

class TestMail(unittest.TestCase):
    @patch.dict(os.environ, {"SMTP_HOST": "smtp.example.com", "SMTP_USER": "user", "SMTP_PASS": "pass"})
    def test_email_validation(self):
        # Longitud mayor a 254
        long_email = "a" * 250 + "@b.com"
        result, msg = send_email(long_email, "Subj", "Body")
        self.assertFalse(result)
        self.assertIn("excede la longitud máxima", msg)

        # Formato inválido
        result, msg = send_email("invalid-email", "Subj", "Body")
        self.assertFalse(result)
        self.assertIn("no es válida", msg)

        # Sin dirección
        result, msg = send_email("", "Subj", "Body")
        self.assertFalse(result)
        self.assertIn("No se ha proporcionado", msg)

if __name__ == '__main__':
    unittest.main()
