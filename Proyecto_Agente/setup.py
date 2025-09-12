#!/usr/bin/env python3
"""
Script de configuración para el Agente de Análisis de Proteínas
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida del error: {e.stderr}")
        return False

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    return True

def create_directories():
    """Crea directorios necesarios"""
    directories = ["logs", "analytics", "reports", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"📁 Directorio '{directory}' creado/verificado")

def create_env_file():
    """Crea archivo .env si no existe"""
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Configuración del Agente de Análisis de Proteínas

# API Key para Hugging Face (REQUERIDO)
# Obtén tu clave en: https://huggingface.co/settings/tokens
HUGGING_FACE_API_KEY=your_hugging_face_api_key_here

# Configuración de Email (OPCIONAL)
# Para envío de reportes por correo
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password_here

# Configuración de Logging
LOG_LEVEL=INFO

# Configuración de Analytics
ENABLE_ANALYTICS=true
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("📝 Archivo .env creado. ¡Recuerda configurar tu API key!")
    else:
        print("✅ Archivo .env ya existe")

def main():
    """Función principal de configuración"""
    print("🔬 Configurando Agente de Análisis de Proteínas")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear directorios
    create_directories()
    
    # Crear archivo .env
    create_env_file()
    
    # Instalar dependencias
    if run_command("pip install -r ../requirements.txt", "Instalando dependencias"):
        print("✅ Todas las dependencias instaladas correctamente")
    else:
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    print("\n🎉 ¡Configuración completada!")
    print("\n📋 Próximos pasos:")
    print("1. Edita el archivo .env y añade tu API key de Hugging Face")
    print("2. Ejecuta: streamlit run src/app.py")
    print("3. ¡Disfruta analizando proteínas con IA!")
    
    # Verificar si se puede importar streamlit
    try:
        import streamlit
        print(f"\n✅ Streamlit {streamlit.__version__} listo para usar")
    except ImportError:
        print("\n❌ Error: No se pudo importar Streamlit")

if __name__ == "__main__":
    main()