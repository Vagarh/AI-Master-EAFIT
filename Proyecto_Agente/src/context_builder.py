"""
Constructor de contexto para conversaciones con el agente de IA.

Este módulo proporciona funcionalidades para construir mensajes estructurados
que incluyen el contexto del análisis de datos, el historial de conversación
y las instrucciones del sistema para el modelo de lenguaje.

Author: Juan Felipe Cardona
Date: 2024
"""

from typing import List, Dict, Optional


def build_messages(
    eda_context: str,
    user_question: str,
    chat_history: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, str]]:
    """
    Construye la lista de mensajes estructurados para el LLM siguiendo un protocolo consistente.

    Este protocolo asegura que el agente siempre reciba:
    1. Un rol del sistema claro (system prompt)
    2. El historial completo de la conversación
    3. El contexto del EDA actual
    4. La pregunta del usuario

    Args:
        eda_context (str): Resumen del Análisis Exploratorio de Datos (estadísticas,
                          información del dataset, etc.)
        user_question (str): Pregunta o mensaje actual del usuario
        chat_history (List[Dict], optional): Lista de mensajes anteriores en el formato
                                            [{"role": "user/assistant", "content": "..."}]

    Returns:
        List[Dict[str, str]]: Lista de mensajes formateados para la API del LLM,
                             listos para ser enviados en la solicitud

    Example:
        >>> messages = build_messages(
        ...     eda_context="Dataset con 1000 secuencias...",
        ...     user_question="¿Cuál es la secuencia más larga?",
        ...     chat_history=[]
        ... )
    """
    # Inicializar historial si no se proporciona
    chat_history = chat_history or []

    # ============================================================
    # Definir el rol del sistema (System Prompt)
    # ============================================================
    system_prompt = (
        "Eres un experto en biología molecular y análisis de datos de proteínas. "
        "Tu rol es actuar como un asistente inteligente para un científico de datos. "
        "Se te proporcionará un contexto sobre un dataset de proteínas y tienes acceso a herramientas bioinformáticas. "
        "\n\n"
        "INSTRUCCIONES DE USO DE HERRAMIENTAS:\n"
        "- Si la pregunta puede responderse con el contexto del EDA, úsalo directamente.\n"
        "- Si la pregunta requiere información externa sobre una secuencia "
        "(ej. '¿a qué se parece esta proteína?'), DEBES usar la herramienta 'run_blast_search'.\n"
        "- Si el usuario pregunta por detalles de una estructura específica usando un ID de 4 caracteres "
        "(ej. 'dame información sobre 2HHB'), DEBES usar la herramienta 'fetch_pdb_data'.\n"
        "\n"
        "ESTILO DE RESPUESTA:\n"
        "- Responde de manera clara, concisa y fundamentada en los datos o en los resultados de las herramientas.\n"
        "- Mantén la memoria de la conversación para responder preguntas de seguimiento.\n"
        "- Usa terminología científica apropiada pero accesible."
    )

    # ============================================================
    # PASO 1: Iniciar con el mensaje del sistema
    # ============================================================
    messages = [{"role": "system", "content": system_prompt}]

    # ============================================================
    # PASO 2: Añadir historial de conversación
    # ============================================================
    # Esto permite al agente mantener contexto de intercambios anteriores
    messages.extend(chat_history)

    # ============================================================
    # PASO 3: Construir el mensaje del usuario con contexto EDA
    # ============================================================
    human_prompt = (
        f"Contexto del EDA (solo para tu referencia, no lo menciones a menos que sea relevante para la pregunta):\n"
        f"--- CONTEXTO ---\n{eda_context}\n--- FIN DEL CONTEXTO ---\n\n"
        f"Pregunta del usuario: {user_question}"
    )
    messages.append({"role": "user", "content": human_prompt})

    return messages
