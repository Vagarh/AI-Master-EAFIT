"""
Sistema de logging para el Agente de Análisis de Proteínas
"""
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logger(name: str = "protein_agent", level: str = "INFO") -> logging.Logger:
    """
    Configura un logger para la aplicación.
    
    Args:
        name: Nombre del logger
        level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya existe
    if logger.handlers:
        return logger
    
    logger.setLevel(getattr(logging, level.upper()))
    
    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para archivo (opcional)
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_dir / f"protein_agent_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        logger.warning(f"No se pudo crear el archivo de log: {e}")
    
    return logger

# Logger global para la aplicación
app_logger = setup_logger()

def log_user_interaction(action: str, details: dict = None):
    """
    Registra interacciones del usuario para análisis posterior.
    
    Args:
        action: Acción realizada (ej: "dataset_loaded", "chat_message", "report_generated")
        details: Detalles adicionales de la acción
    """
    details = details or {}
    app_logger.info(f"USER_ACTION: {action} | Details: {details}")

def log_agent_response(question: str, response_length: int, tools_used: list = None):
    """
    Registra respuestas del agente para monitoreo.
    
    Args:
        question: Pregunta del usuario
        response_length: Longitud de la respuesta
        tools_used: Lista de herramientas utilizadas
    """
    tools_used = tools_used or []
    app_logger.info(
        f"AGENT_RESPONSE: Question length: {len(question)} | "
        f"Response length: {response_length} | Tools: {tools_used}"
    )

def log_error(error: Exception, context: str = ""):
    """
    Registra errores con contexto adicional.
    
    Args:
        error: Excepción capturada
        context: Contexto donde ocurrió el error
    """
    app_logger.error(f"ERROR in {context}: {type(error).__name__}: {str(error)}")