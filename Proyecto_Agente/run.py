#!/usr/bin/env python3
"""
Script de inicio para el Agente de Análisis de Proteínas
"""
import os
import sys
import subprocess
from pathlib import Path
import webbrowser
import time

def check_requirements():
    """Verifica que los requisitos estén instalados"""
    try:
        import streamlit
        import pandas
        import matplotlib
        import litellm
        print("✅ Todas las dependencias principales están instaladas")
        return True
    except ImportError as e:
        print(f"❌ Falta dependencia: {e}")
        print("💡 Ejecuta: python setup.py para instalar dependencias")
        return False

def check_env_file():
    """Verifica la configuración del archivo .env"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Archivo .env no encontrado")
        print("💡 Ejecuta: python setup.py para crear la configuración")
        return False
    
    # Verificar API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("HUGGING_FACE_API_KEY")
    if not api_key or api_key == "your_hugging_face_api_key_here":
        print("⚠️  API Key de Hugging Face no configurada")
        print("💡 Edita el archivo .env y añade tu API key")
        return False
    
    print("✅ Configuración verificada")
    return True

def start_streamlit():
    """Inicia la aplicación Streamlit"""
    app_path = Path("src/app.py")
    if not app_path.exists():
        print("❌ No se encontró src/app.py")
        return False
    
    print("🚀 Iniciando Agente de Análisis de Proteínas...")
    print("📱 La aplicación se abrirá en tu navegador")
    print("🔗 URL: http://localhost:8501")
    print("\n⏹️  Presiona Ctrl+C para detener la aplicación")
    
    try:
        # Iniciar Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path),
            "--server.port=8501",
            "--server.address=localhost",
            "--browser.gatherUsageStats=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 ¡Aplicación detenida!")
    except Exception as e:
        print(f"❌ Error iniciando la aplicación: {e}")
        return False
    
    return True

def show_help():
    """Muestra información de ayuda"""
    help_text = """
🔬 Agente de Análisis de Proteínas - Ayuda

📋 Comandos disponibles:
  python run.py          - Inicia la aplicación
  python run.py --help   - Muestra esta ayuda
  python run.py --check  - Verifica la configuración
  python setup.py        - Configura el entorno

🔧 Solución de problemas:
  1. Si faltan dependencias: python setup.py
  2. Si falta API key: edita el archivo .env
  3. Si hay errores de puerto: cambia el puerto en el código

📚 Documentación:
  - README.md: Información completa del proyecto
  - .env.example: Ejemplo de configuración
  - src/: Código fuente de la aplicación

🆘 Soporte:
  - GitHub: https://github.com/Vagarh/AI-Master-EAFIT
  - Issues: Reporta problemas en GitHub
    """
    print(help_text)

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help":
            show_help()
            return
        elif sys.argv[1] == "--check":
            print("🔍 Verificando configuración...")
            deps_ok = check_requirements()
            env_ok = check_env_file()
            if deps_ok and env_ok:
                print("✅ Todo está listo para ejecutar")
            else:
                print("❌ Hay problemas de configuración")
            return
    
    print("🔬 Agente de Análisis de Proteínas")
    print("=" * 40)
    
    # Verificaciones previas
    if not check_requirements():
        sys.exit(1)
    
    if not check_env_file():
        print("\n⚠️  Puedes continuar, pero el agente de IA no funcionará")
        response = input("¿Continuar de todos modos? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Iniciar aplicación
    start_streamlit()

if __name__ == "__main__":
    main()