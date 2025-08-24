import os
import json
from litellm import completion
from tools import run_blast_search
from context_builder import build_messages

class ProteinAnalysisAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key
        if not self.api_key:
            self.api_key = os.getenv("HUGGING_FACE_API_KEY")
        if not self.api_key:
            raise ValueError("API key for Hugging Face not found. Please provide it in the UI or set the HUGGING_FACE_API_KEY environment variable.")

    def chat(self, context: str, user_question: str, chat_history: list = None):
        """
        Genera una respuesta utilizando un LLM. El agente puede decidir usar herramientas
        como BLAST para responder preguntas y mantiene el contexto de la conversación.
        """
        chat_history = chat_history or []
        # 1. Definir las herramientas disponibles para esta llamada
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

        # 2. Construir los mensajes usando el nuevo protocolo
        messages = build_messages(
            eda_context=context,
            user_question=user_question,
            chat_history=chat_history
        )
        
        try:
            # 3. Primera llamada: El LLM decide si usa una herramienta
            response = completion(
                model="huggingface/together/deepseek-ai/DeepSeek-R1",
                messages=messages,
                tools=tools,
                tool_choice="auto",
                api_key=self.api_key
            )

            response_message = response.choices[0].message

            # 4. Segunda etapa: Ejecutar la herramienta si el LLM lo solicita
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
