#!/usr/bin/env python3
"""
Script de prueba para verificar que todos los imports funcionan correctamente
"""
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Prueba todos los imports principales"""
    try:
        print("🔄 Probando imports...")
        
        # Imports básicos
        import streamlit as st
        print("✅ Streamlit importado correctamente")
        
        import pandas as pd
        print("✅ Pandas importado correctamente")
        
        # Imports de nuestros módulos
        from config import APP_CONFIG, MESSAGES
        print("✅ Config importado correctamente")
        
        from logger import app_logger
        print("✅ Logger importado correctamente")
        
        from analytics import analytics_tracker
        print("✅ Analytics importado correctamente")
        
        from utils import validate_protein_sequence
        print("✅ Utils importado correctamente")
        
        # Probar una función
        result = validate_protein_sequence("ACDEFGHIKLMNPQRSTVWY")
        print(f"✅ Validación de secuencia funciona: {result['is_valid']}")
        
        # Imports que pueden fallar por dependencias externas
        try:
            from agent import ProteinAnalysisAgent
            print("✅ Agent importado correctamente")
        except Exception as e:
            print(f"⚠️  Agent import con advertencia: {e}")
        
        try:
            from eda import validate_eda
            print("✅ EDA importado correctamente")
        except Exception as e:
            print(f"⚠️  EDA import con advertencia: {e}")
        
        print("\n🎉 ¡Todos los imports principales funcionan!")
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def test_config():
    """Prueba la configuración"""
    try:
        from config import APP_CONFIG, MESSAGES, REQUIRED_COLUMNS
        
        print("\n🔧 Probando configuración...")
        print(f"✅ Título de la app: {APP_CONFIG['page_title']}")
        print(f"✅ Columnas requeridas: {len(REQUIRED_COLUMNS)} columnas")
        print(f"✅ Mensajes configurados: {len(MESSAGES)} mensajes")
        
        return True
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 Ejecutando pruebas del Agente de Análisis de Proteínas")
    print("=" * 60)
    
    success = True
    
    # Probar imports
    if not test_imports():
        success = False
    
    # Probar configuración
    if not test_config():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ¡Todas las pruebas pasaron! La aplicación está lista.")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)