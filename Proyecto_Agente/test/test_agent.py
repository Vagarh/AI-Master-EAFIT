
import unittest
from unittest.mock import patch, MagicMock
import os
from src.agent import ProteinAnalysisAgent

class TestProteinAnalysisAgent(unittest.TestCase):

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    def test_init_success(self):
        """
        Prueba que el agente se inicializa correctamente cuando la API key existe.
        """
        try:
            agent = ProteinAnalysisAgent()
            self.assertIsInstance(agent, ProteinAnalysisAgent)
            self.assertEqual(agent.api_key, "test_key")
        except ValueError:
            self.fail("ProteinAnalysisAgent raised ValueError unexpectedly!")

    @patch.dict(os.environ, {}, clear=True)
    def test_init_no_api_key(self):
        """
        Prueba que se lanza un ValueError si la API key no está configurada.
        """
        with self.assertRaises(ValueError) as context:
            ProteinAnalysisAgent()
        self.assertIn("API key for Gemini not found", str(context.exception))

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("src.agent.completion")
    def test_chat_success(self, mock_completion):
        """
        Prueba una llamada exitosa al método chat, mockeando la respuesta de la API.
        """
        # Configurar el mock para simular una respuesta exitosa de la API
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "Respuesta simulada de la IA"
        mock_completion.return_value = mock_response

        agent = ProteinAnalysisAgent()
        context = "Este es un contexto de prueba."
        user_question = "¿Cuál es la respuesta?"
        
        response = agent.chat(context, user_question)

        # Verificar que la respuesta es la que esperamos del mock
        self.assertEqual(response, "Respuesta simulada de la IA")

        # Verificar que la función de completion fue llamada con los argumentos correctos
        mock_completion.assert_called_once()
        args, kwargs = mock_completion.call_args
        self.assertEqual(kwargs['model'], "gemini/gemini-pro")
        self.assertEqual(kwargs['api_key'], "test_key")
        
        messages = kwargs['messages']
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]['role'], "system")
        self.assertIn("experto en biología molecular", messages[0]['content'])
        self.assertEqual(messages[1]['role'], "user")
        self.assertIn(context, messages[1]['content'])
        self.assertIn(user_question, messages[1]['content'])

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_key"})
    @patch("src.agent.completion")
    def test_chat_api_error(self, mock_completion):
        """
        Prueba cómo maneja el método chat una excepción de la API.
        """
        # Configurar el mock para que lance una excepción
        mock_completion.side_effect = Exception("Error de red simulado")

        agent = ProteinAnalysisAgent()
        context = "Contexto de prueba."
        user_question = "Pregunta de prueba."

        response = agent.chat(context, user_question)

        # Verificar que la respuesta contiene el mensaje de error esperado
        self.assertIn("Error al contactar el modelo de lenguaje: Error de red simulado", response)

if __name__ == "__main__":
    unittest.main()
