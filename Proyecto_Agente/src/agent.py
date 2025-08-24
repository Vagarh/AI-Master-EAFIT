import os
import json
from litellm import completion
from tools import run_blast_search

class ProteinAnalysisAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.getenv("HUGGING_FACE_API_KEY")
        if not self.api_key:
            raise ValueError("API key for Hugging Face not found. Please provide it in the UI or set the HUGGING_FACE_API_KEY environment variable.")

    def chat(self, context, user_question):
        """
        Genera una respuesta utilizando un LLM. El agente puede decidir usar herramientas
        como BLAST para responder preguntas que van más allá del contexto del EDA.
        """
        # 1. Definir las herramientas que el agente puede usar
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "run_blast_search",
                    "description": "Realiza una búsqueda BLAST para una secuencia de proteína dada contra la base de datos 'nr' de NCBI para encontrar secuencias similares.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sequence": {
                                "type": "string",
                                "description": "La secuencia de proteína para la cual realizar la búsqueda. Debe ser una cadena de aminoácidos válida.",
                            },
                            "top_n": {
                                "type": "integer",
                                "description": "El número de los mejores resultados a devolver. El valor por defecto es 3.",
                                "default": 3
                            }
                        },
                        "required": ["sequence"],
                    },
                },
            }
        ]

        system_prompt = (
            "Eres un experto en biología molecular y análisis de datos de proteínas. "
            "Tu rol es actuar como un asistente inteligente para un científico de datos. "
            "Se te proporcionará un contexto que consiste en un Análisis Exploratorio de Datos (EDA) de un dataset de proteínas. "
            "También tienes acceso a herramientas bioinformáticas como BLAST. "
            "Si la pregunta del usuario puede ser respondida con el contexto del EDA, úsalo. "
            "Si la pregunta requiere información externa sobre una secuencia específica (ej. '¿qué función tiene esta secuencia?', '¿a qué se parece esta proteína?'), "
            "DEBES usar la herramienta 'run_blast_search'. "
            "Responde de manera clara, concisa y fundamentada en los datos o en los resultados de las herramientas."
        )
        
        human_prompt = (
            f"Contexto del EDA:\n"
            f"--- CONTEXTO ---\n"
            f"{context}\n"
            f"--- FIN DEL CONTEXTO ---\n\n"
            f"Pregunta del usuario: {user_question}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": human_prompt}
        ]
        
        try:
            # 2. Primera llamada: El LLM decide si usa una herramienta
            response = completion(
                model="huggingface/together/deepseek-ai/DeepSeek-R1",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                api_key=self.api_key
            )

            response_message = response.choices[0].message

            # 3. Segunda etapa: Ejecutar la herramienta si el LLM lo solicita
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "run_blast_search":
                    tool_result = run_blast_search(
                        sequence=function_args.get("sequence"),
                        top_n=function_args.get("top_n", 3)
                    )
                    messages.append(response_message)
                    messages.append({"role": "tool", "tool_call_id": tool_call.id, "name": function_name, "content": tool_result})
                    final_response = completion(model="huggingface/together/deepseek-ai/DeepSeek-R1", messages=messages, api_key=self.api_key)
                    return final_response.choices[0].message.content
                else:
                    return f"Error: El modelo intentó llamar a una herramienta desconocida: {function_name}"

            # Si no se usó ninguna herramienta, devolver la respuesta directa
            return response_message.content

        except Exception as e:
            return f"Error al procesar la solicitud con el agente: {e}"
