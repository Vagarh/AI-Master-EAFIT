import unittest
import os
from unittest.mock import patch, MagicMock

from Proyecto_Agente.src.mail import send_email

class TestMailValidation(unittest.TestCase):
    @patch('Proyecto_Agente.src.mail.smtplib.SMTP')
    @patch.dict(os.environ, {"SMTP_HOST": "test", "SMTP_USER": "user", "SMTP_PASS": "pass", "SMTP_PORT": "587"})
    def test_send_email_validation(self, mock_smtp):
        # Mock SMTP connection and methods to avoid real network calls
        mock_smtp_instance = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_smtp_instance

        # Email format is correct
        self.assertNotIn("Error", send_email("valid@email.com", "Subj", "Body")[1])

        # Length is over 254
        long_email = "a" * 200 + "@" + "b" * 50 + ".com"
        self.assertIn("excede el tamaño máximo", send_email(long_email, "Subj", "Body")[1])

        # Missing @
        self.assertIn("no es válida", send_email("invalidemail.com", "Subj", "Body")[1])

        # Missing domain extension
        self.assertIn("no es válida", send_email("invalid@email", "Subj", "Body")[1])

if __name__ == '__main__':
    unittest.main()
