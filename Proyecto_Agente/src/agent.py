import os
from litellm import completion

class ProteinAnalysisAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.getenv("HUGGING_FACE_API_KEY")
        if not self.api_key:
            raise ValueError("API key for Hugging Face not found. Please provide it in the UI or set the HUGGING_FACE_API_KEY environment variable.")

    def chat(self, context, user_question):
        """
        Genera una respuesta utilizando un LLM basado en el contexto del EDA y la pregunta del usuario.
        """
        system_prompt = (
            "Eres un experto en biología molecular y análisis de datos de proteínas. "
            "Tu rol es actuar como un asistente inteligente para un científico de datos. "
            "Se te proporcionará un contexto que consiste en un Análisis Exploratorio de Datos (EDA) de un dataset de proteínas. "
            "Basado en este contexto, debes responder a las preguntas del usuario de manera clara, concisa y fundamentada en los datos."
            "No inventes información que no esté en el contexto."
        )
        
        human_prompt = (
            f"Aquí está el contexto del EDA:\n"
            f"--- CONTEXTO ---\n"
            f"{context}\n"
            f"--- FIN DEL CONTEXTO ---\n\n"
            f"Basado en el contexto anterior, por favor responde la siguiente pregunta:\n"
            f"Pregunta: {user_question}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ]

        try:
            response = completion(
                model="huggingface/together/deepseek-ai/DeepSeek-R1", 
                messages=messages,
                api_key=self.api_key
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error al contactar el modelo de lenguaje: {e}"
