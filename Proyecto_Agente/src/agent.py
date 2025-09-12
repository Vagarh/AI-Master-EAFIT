import os
import json
from litellm import completion
from tools import run_blast_search, fetch_pdb_data
from context_builder import build_messages
from logger import app_logger, log_agent_response, log_error
from config import MODEL_CONFIG

class ProteinAnalysisAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv(MODEL_CONFIG["api_key_env"])
        self.model_name = MODEL_CONFIG["model_name"]
        
        if not self.api_key:
            raise ValueError(
                f"API key for Hugging Face not found. "
                f"Please set the {MODEL_CONFIG['api_key_env']} environment variable."
            )
        
        app_logger.info(f"ProteinAnalysisAgent initialized with model: {self.model_name}")

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
            },
            {
                "type": "function",
                "function": {
                    "name": "fetch_pdb_data",
                    "description": "Busca y devuelve metadatos para un ID de PDB específico (ej. '2HHB') desde la base de datos de RCSB PDB.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "pdb_id": {
                                "type": "string",
                                "description": "El ID de 4 caracteres del Protein Data Bank a buscar.",
                            }
                        },
                        "required": ["pdb_id"],
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
        
        tools_used = []
        
        try:
            app_logger.debug(f"Processing question: {user_question[:100]}...")
            
            # 3. Primera llamada: El LLM decide si usa una herramienta
            response = completion(
                model=self.model_name,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                api_key=self.api_key,
                max_tokens=MODEL_CONFIG.get("max_tokens", 4000),
                temperature=MODEL_CONFIG.get("temperature", 0.1)
            )

            response_message = response.choices[0].message

            # 4. Segunda etapa: Ejecutar la herramienta si el LLM lo solicita
            if response_message.tool_calls:
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                app_logger.info(f"Agent using tool: {function_name} with args: {function_args}")
                tools_used.append(function_name)

                try:
                    if function_name == "run_blast_search":
                        tool_result = run_blast_search(
                            sequence=function_args.get("sequence"),
                            top_n=function_args.get("top_n", 3)
                        )
                        messages.append(response_message)
                        messages.append({
                            "role": "tool", 
                            "tool_call_id": tool_call.id, 
                            "name": function_name, 
                            "content": tool_result
                        })
                        
                    elif function_name == "fetch_pdb_data":
                        tool_result = fetch_pdb_data(
                            pdb_id=function_args.get("pdb_id")
                        )
                        messages.append(response_message)
                        messages.append({
                            "role": "tool", 
                            "tool_call_id": tool_call.id, 
                            "name": function_name, 
                            "content": tool_result
                        })
                        
                    else:
                        error_msg = f"Error: El modelo intentó llamar a una herramienta desconocida: {function_name}"
                        app_logger.error(error_msg)
                        return error_msg
                    
                    # Segunda llamada para procesar el resultado de la herramienta
                    final_response = completion(
                        model=self.model_name, 
                        messages=messages, 
                        api_key=self.api_key,
                        max_tokens=MODEL_CONFIG.get("max_tokens", 4000),
                        temperature=MODEL_CONFIG.get("temperature", 0.1)
                    )
                    final_content = final_response.choices[0].message.content
                    
                    # Log de la respuesta
                    log_agent_response(user_question, len(final_content), tools_used)
                    return final_content
                    
                except Exception as tool_error:
                    log_error(tool_error, f"tool_execution_{function_name}")
                    return f"Error al ejecutar la herramienta {function_name}: {str(tool_error)}"

            # Si no se usó ninguna herramienta, devolver la respuesta directa
            final_content = response_message.content
            log_agent_response(user_question, len(final_content), tools_used)
            return final_content

        except Exception as e:
            log_error(e, "agent_chat")
            return f"Error al procesar la solicitud con el agente: {str(e)}"
