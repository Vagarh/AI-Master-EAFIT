"""
Agente de análisis de proteínas con capacidades de IA conversacional.

Este módulo implementa un agente inteligente que utiliza modelos de lenguaje (LLM)
para responder preguntas sobre datasets de proteínas. El agente puede:
- Analizar datos de proteínas usando contexto EDA
- Realizar búsquedas BLAST para encontrar secuencias similares
- Consultar información de estructuras cristalográficas en PDB
- Mantener el contexto de conversaciones

Author: Juan Felipe Cardona
Date: 2024
"""

import os
import json
from typing import List, Dict, Optional
from litellm import completion

# Importaciones locales
from tools import run_blast_search, fetch_pdb_data
from context_builder import build_messages
from logger import app_logger, log_agent_response, log_error
from config import MODEL_CONFIG


class ProteinAnalysisAgent:
    """
    Agente conversacional especializado en análisis de proteínas.

    Este agente combina capacidades de procesamiento de lenguaje natural con
    herramientas bioinformáticas para proporcionar análisis inteligentes de
    datos de proteínas.

    Attributes:
        api_key (str): Clave de API para autenticación con el servicio LLM
        model_name (str): Nombre del modelo de lenguaje a utilizar
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa el agente de análisis de proteínas.

        Args:
            api_key (str, optional): Clave de API para Hugging Face. Si no se proporciona,
                                    se intentará obtener de las variables de entorno.

        Raises:
            ValueError: Si no se encuentra una API key válida
        """
        # Obtener la API key de los parámetros o variables de entorno
        self.api_key = api_key or os.getenv(MODEL_CONFIG["api_key_env"])
        self.model_name = MODEL_CONFIG["model_name"]

        # Validar que la API key esté disponible
        if not self.api_key:
            raise ValueError(
                f"API key for Hugging Face not found. "
                f"Please set the {MODEL_CONFIG['api_key_env']} environment variable."
            )

        app_logger.info(f"ProteinAnalysisAgent initialized with model: {self.model_name}")

    def chat(self, context: str, user_question: str, chat_history: Optional[List[Dict]] = None) -> str:
        """
        Genera una respuesta inteligente usando el LLM con acceso a herramientas bioinformáticas.

        El agente utiliza un patrón de dos etapas:
        1. Primera llamada: El LLM decide si necesita usar herramientas
        2. Segunda llamada (si aplica): Procesa los resultados de las herramientas

        Args:
            context (str): Contexto del análisis exploratorio de datos (EDA)
            user_question (str): Pregunta actual del usuario
            chat_history (List[Dict], optional): Historial de mensajes anteriores

        Returns:
            str: Respuesta generada por el agente

        Raises:
            Exception: Si ocurre un error durante la generación de la respuesta
        """
        chat_history = chat_history or []

        # ============================================================
        # PASO 1: Definir herramientas bioinformáticas disponibles
        # ============================================================
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

        # ============================================================
        # PASO 2: Construir los mensajes con contexto completo
        # ============================================================
        messages = build_messages(
            eda_context=context,
            user_question=user_question,
            chat_history=chat_history
        )

        # Registro de herramientas utilizadas para analytics
        tools_used = []

        try:
            app_logger.debug(f"Processing question: {user_question[:100]}...")

            # ============================================================
            # PASO 3: Primera llamada al LLM - Decisión de uso de herramientas
            # ============================================================
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

            # ============================================================
            # PASO 4: Ejecutar herramientas si el LLM las solicita
            # ============================================================
            if response_message.tool_calls:
                # Extraer información de la llamada a la herramienta
                tool_call = response_message.tool_calls[0]
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Logging para monitoreo y debugging
                app_logger.info(f"Agent using tool: {function_name} with args: {function_args}")
                tools_used.append(function_name)

                try:
                    # Ejecutar la herramienta apropiada según el tipo
                    if function_name == "run_blast_search":
                        # Búsqueda de secuencias similares en NCBI
                        tool_result = run_blast_search(
                            sequence=function_args.get("sequence"),
                            top_n=function_args.get("top_n", 3)
                        )
                        # Añadir el mensaje de la herramienta al contexto
                        messages.append(response_message)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": tool_result
                        })

                    elif function_name == "fetch_pdb_data":
                        # Obtener metadatos de estructura cristalográfica
                        tool_result = fetch_pdb_data(
                            pdb_id=function_args.get("pdb_id")
                        )
                        # Añadir el mensaje de la herramienta al contexto
                        messages.append(response_message)
                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": tool_result
                        })

                    else:
                        # Herramienta desconocida - registrar error
                        error_msg = f"Error: El modelo intentó llamar a una herramienta desconocida: {function_name}"
                        app_logger.error(error_msg)
                        return error_msg

                    # ============================================================
                    # PASO 5: Segunda llamada al LLM - Procesar resultado de herramienta
                    # ============================================================
                    final_response = completion(
                        model=self.model_name,
                        messages=messages,
                        api_key=self.api_key,
                        max_tokens=MODEL_CONFIG.get("max_tokens", 4000),
                        temperature=MODEL_CONFIG.get("temperature", 0.1)
                    )
                    final_content = final_response.choices[0].message.content

                    # Registrar la respuesta para analytics
                    log_agent_response(user_question, len(final_content), tools_used)
                    return final_content

                except Exception as tool_error:
                    # Manejo de errores en la ejecución de herramientas
                    log_error(tool_error, f"tool_execution_{function_name}")
                    return f"Error al ejecutar la herramienta {function_name}: {str(tool_error)}"

            # ============================================================
            # PASO 6: Respuesta directa (sin herramientas)
            # ============================================================
            # Si el LLM no solicitó herramientas, devolver su respuesta directa
            final_content = response_message.content
            log_agent_response(user_question, len(final_content), tools_used)
            return final_content

        except Exception as e:
            # Manejo de errores generales en el chat
            log_error(e, "agent_chat")
            return f"Error al procesar la solicitud con el agente: {str(e)}"
