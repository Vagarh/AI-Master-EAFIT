#!/usr/bin/env python3
"""
Script de demostración del Agente de Análisis de Proteínas
"""
import sys
import os
import pandas as pd

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_features():
    """Demuestra las características principales de la aplicación"""
    print("🔬 DEMOSTRACIÓN: Agente de Análisis de Proteínas")
    print("=" * 60)
    
    # 1. Configuración
    print("\n1️⃣ CONFIGURACIÓN")
    print("-" * 20)
    try:
        from config import APP_CONFIG, MESSAGES, REQUIRED_COLUMNS
        print(f"✅ Título: {APP_CONFIG['page_title']}")
        print(f"✅ Columnas requeridas: {', '.join(REQUIRED_COLUMNS)}")
        print(f"✅ Mensajes configurados: {len(MESSAGES)}")
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
    
    # 2. Utilidades
    print("\n2️⃣ UTILIDADES DE VALIDACIÓN")
    print("-" * 30)
    try:
        from utils import validate_protein_sequence, calculate_molecular_weight
        
        # Probar validación de secuencia
        test_seq = "ACDEFGHIKLMNPQRSTVWY"
        validation = validate_protein_sequence(test_seq)
        print(f"✅ Secuencia válida: {validation['is_valid']}")
        print(f"✅ Longitud: {validation['length']} aminoácidos")
        
        # Probar cálculo de peso molecular
        weight = calculate_molecular_weight(test_seq)
        print(f"✅ Peso molecular: {weight:.2f} Da")
        
    except Exception as e:
        print(f"❌ Error en utilidades: {e}")
    
    # 3. Analytics
    print("\n3️⃣ SISTEMA DE ANALYTICS")
    print("-" * 25)
    try:
        from analytics import analytics_tracker, get_dataset_insights
        
        # Simular evento
        analytics_tracker.track_event("demo_test", {"feature": "validation"})
        print("✅ Evento de analytics registrado")
        
        # Crear dataset de ejemplo
        sample_data = {
            'seq': ['ACDEFG', 'HIKLMN', 'PQRSTV'],
            'sst3': ['HHHEEE', 'CCCHHE', 'EEECCC'],
            'sst8': ['HHHEEE', 'CCCHHE', 'EEECCC'],
            'len': [6, 6, 6],
            'has_nonstd_aa': [False, False, True]
        }
        df_sample = pd.DataFrame(sample_data)
        
        insights = get_dataset_insights(df_sample)
        print(f"✅ Insights generados: {len(insights)} categorías")
        
    except Exception as e:
        print(f"❌ Error en analytics: {e}")
    
    # 4. Logging
    print("\n4️⃣ SISTEMA DE LOGGING")
    print("-" * 22)
    try:
        from logger import app_logger, log_user_interaction
        
        app_logger.info("Demo del sistema de logging")
        log_user_interaction("demo_test", {"timestamp": "now"})
        print("✅ Sistema de logging funcionando")
        
    except Exception as e:
        print(f"❌ Error en logging: {e}")
    
    # 5. EDA
    print("\n5️⃣ ANÁLISIS EXPLORATORIO")
    print("-" * 25)
    try:
        from eda import validate_eda
        
        # Usar el mismo dataset de ejemplo
        is_valid = validate_eda(df_sample)
        print(f"✅ Dataset válido para EDA: {is_valid}")
        
    except Exception as e:
        print(f"❌ Error en EDA: {e}")
    
    # 6. Agente (sin API key)
    print("\n6️⃣ AGENTE DE IA")
    print("-" * 15)
    try:
        from agent import ProteinAnalysisAgent
        print("⚠️  Agente disponible (requiere API key para funcionar)")
        
    except Exception as e:
        print(f"❌ Error en agente: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 DEMOSTRACIÓN COMPLETADA")
    print("\n📋 RESUMEN DE CARACTERÍSTICAS:")
    print("   ✅ Configuración modular")
    print("   ✅ Validación de secuencias de proteínas")
    print("   ✅ Cálculo de peso molecular")
    print("   ✅ Sistema de analytics y métricas")
    print("   ✅ Logging estructurado")
    print("   ✅ Análisis exploratorio de datos")
    print("   ✅ Interfaz web con Streamlit")
    print("   ⚠️  Agente de IA (requiere configuración)")
    
    print("\n🚀 PARA USAR LA APLICACIÓN:")
    print("   1. Configura tu API key en .env")
    print("   2. Ejecuta: streamlit run src/app.py")
    print("   3. Abre http://localhost:8501 en tu navegador")

if __name__ == "__main__":
    demo_features()