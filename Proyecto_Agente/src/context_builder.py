from typing import List, Dict

def build_messages(
    eda_context: str,
    user_question: str,
    chat_history: List[Dict[str, str]] = None
) -> List[Dict[str, str]]:
    """
    Construye la lista de mensajes para el LLM siguiendo un protocolo estructurado.

    Este "protocolo" asegura que el agente siempre reciba un contexto consistente
    que incluye su persona (rol del sistema), el historial de la conversación,
    el contexto de los datos (EDA) y la pregunta actual del usuario.

    Args:
        eda_context: Un string con el resumen del Análisis Exploratorio de Datos.
        user_question: La pregunta actual del usuario.
        chat_history: Una lista de mensajes anteriores en la conversación.

    Returns:
        Una lista de diccionarios, cada uno representando un mensaje en el formato
        que espera la API del LLM.
    """
    chat_history = chat_history or []

    system_prompt = (
        "Eres un experto en biología molecular y análisis de datos de proteínas. "
        "Tu rol es actuar como un asistente inteligente para un científico de datos. "
        "Se te proporcionará un contexto que consiste en un Análisis Exploratorio de Datos (EDA) de un dataset de proteínas. "
        "También tienes acceso a herramientas bioinformáticas como BLAST. "
        "Si la pregunta del usuario puede ser respondida con el contexto del EDA, úsalo. "
        "Si la pregunta requiere información externa sobre una secuencia específica (ej. '¿qué función tiene esta secuencia?', '¿a qué se parece esta proteína?'), "
        "DEBES usar la herramienta 'run_blast_search'. "
        "Responde de manera clara, concisa y fundamentada en los datos o en los resultados de las herramientas. "
        "Mantén la memoria de la conversación para responder preguntas de seguimiento."
    )
    
    # 1. Empezar con el rol del sistema
    messages = [{"role": "system", "content": system_prompt}]

    # 2. Añadir el historial de la conversación para darle memoria al agente
    messages.extend(chat_history)

    # 3. Construir y añadir el prompt del usuario actual, que incluye el contexto del EDA
    human_prompt = (
        f"Contexto del EDA (solo para tu referencia, no lo menciones a menos que sea relevante para la pregunta):\n"
        f"--- CONTEXTO ---\n{eda_context}\n--- FIN DEL CONTEXTO ---\n\n"
        f"Pregunta del usuario: {user_question}"
    )
    messages.append({"role": "user", "content": human_prompt})
    
    return messages