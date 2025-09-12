"""
Sistema de métricas y analytics para el Agente de Análisis de Proteínas
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path

class AnalyticsTracker:
    """Rastrea y analiza el uso de la aplicación"""
    
    def __init__(self):
        self.analytics_file = Path("analytics/usage_data.json")
        self.analytics_file.parent.mkdir(exist_ok=True)
        
    def track_event(self, event_type: str, data: dict = None):
        """
        Registra un evento de uso.
        
        Args:
            event_type: Tipo de evento (dataset_loaded, chat_message, tool_used, etc.)
            data: Datos adicionales del evento
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "session_id": st.session_state.get("session_id", "unknown"),
            "data": data or {}
        }
        
        # Cargar eventos existentes
        events = self._load_events()
        events.append(event)
        
        # Guardar eventos actualizados
        self._save_events(events)
    
    def _load_events(self) -> list:
        """Carga eventos existentes del archivo"""
        try:
            if self.analytics_file.exists():
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return []
    
    def _save_events(self, events: list):
        """Guarda eventos en el archivo"""
        try:
            with open(self.analytics_file, 'w') as f:
                json.dump(events[-1000:], f, indent=2)  # Mantener solo los últimos 1000 eventos
        except Exception:
            pass
    
    def get_usage_stats(self) -> dict:
        """Obtiene estadísticas de uso"""
        events = self._load_events()
        if not events:
            return {}
        
        df = pd.DataFrame(events)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Estadísticas básicas
        stats = {
            "total_events": len(df),
            "unique_sessions": df['session_id'].nunique(),
            "date_range": {
                "start": df['timestamp'].min().isoformat(),
                "end": df['timestamp'].max().isoformat()
            },
            "event_types": df['event_type'].value_counts().to_dict(),
            "daily_usage": df.groupby(df['timestamp'].dt.date).size().to_dict()
        }
        
        return stats

def create_usage_dashboard():
    """Crea un dashboard de uso de la aplicación"""
    tracker = AnalyticsTracker()
    stats = tracker.get_usage_stats()
    
    if not stats:
        st.info("No hay datos de uso disponibles aún.")
        return
    
    st.subheader("📊 Analytics de Uso")
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Eventos", stats["total_events"])
    col2.metric("Sesiones Únicas", stats["unique_sessions"])
    col3.metric("Días Activos", len(stats["daily_usage"]))
    col4.metric("Promedio Eventos/Día", f"{stats['total_events'] / max(len(stats['daily_usage']), 1):.1f}")
    
    # Gráfico de eventos por tipo
    if stats["event_types"]:
        fig_events = px.pie(
            values=list(stats["event_types"].values()),
            names=list(stats["event_types"].keys()),
            title="Distribución de Tipos de Eventos"
        )
        st.plotly_chart(fig_events, use_container_width=True)
    
    # Gráfico de uso diario
    if stats["daily_usage"]:
        daily_df = pd.DataFrame([
            {"date": date, "events": count} 
            for date, count in stats["daily_usage"].items()
        ])
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        
        fig_daily = px.line(
            daily_df, 
            x="date", 
            y="events",
            title="Uso Diario de la Aplicación",
            markers=True
        )
        st.plotly_chart(fig_daily, use_container_width=True)

def get_dataset_insights(df: pd.DataFrame) -> dict:
    """
    Genera insights automáticos del dataset.
    
    Args:
        df: DataFrame con los datos de proteínas
        
    Returns:
        Diccionario con insights del dataset
    """
    if df is None or df.empty:
        return {}
    
    insights = {}
    
    # Insights básicos
    insights["basic"] = {
        "total_sequences": len(df),
        "avg_length": df['len'].mean() if 'len' in df.columns else None,
        "length_range": {
            "min": df['len'].min() if 'len' in df.columns else None,
            "max": df['len'].max() if 'len' in df.columns else None
        }
    }
    
    # Insights de estructura secundaria
    if 'sst3' in df.columns:
        all_structures = ''.join(df['sst3'])
        structure_counts = pd.Series(list(all_structures)).value_counts()
        insights["secondary_structure"] = {
            "most_common": structure_counts.index[0] if len(structure_counts) > 0 else None,
            "distribution": structure_counts.to_dict()
        }
    
    # Insights de calidad
    if 'has_nonstd_aa' in df.columns:
        nonstd_pct = (df['has_nonstd_aa'].sum() / len(df)) * 100
        insights["quality"] = {
            "nonstd_aa_percentage": nonstd_pct,
            "high_quality_sequences": len(df[~df['has_nonstd_aa']]) if 'has_nonstd_aa' in df.columns else None
        }
    
    # Insights de longitud
    if 'len' in df.columns:
        length_categories = pd.cut(df['len'], bins=[0, 100, 300, 500, float('inf')], 
                                 labels=['Corta (<100)', 'Media (100-300)', 'Larga (300-500)', 'Muy Larga (>500)'])
        insights["length_categories"] = length_categories.value_counts().to_dict()
    
    return insights

def display_insights_panel(df: pd.DataFrame):
    """Muestra un panel de insights automáticos"""
    insights = get_dataset_insights(df)
    
    if not insights:
        return
    
    st.subheader("🔍 Insights Automáticos")
    
    # Insights básicos
    if "basic" in insights:
        basic = insights["basic"]
        st.markdown(f"""
        **📊 Resumen del Dataset:**
        - Total de secuencias: **{basic['total_sequences']:,}**
        - Longitud promedio: **{basic['avg_length']:.1f} aminoácidos**
        - Rango de longitudes: **{basic['length_range']['min']} - {basic['length_range']['max']} AA**
        """)
    
    # Insights de estructura
    if "secondary_structure" in insights:
        struct = insights["secondary_structure"]
        structure_names = {"H": "Hélice α", "E": "Hoja β", "C": "Coil/Loop"}
        most_common_name = structure_names.get(struct["most_common"], struct["most_common"])
        st.markdown(f"""
        **🧬 Estructura Secundaria:**
        - Estructura más común: **{most_common_name}**
        """)
    
    # Insights de calidad
    if "quality" in insights:
        quality = insights["quality"]
        st.markdown(f"""
        **✅ Calidad del Dataset:**
        - Secuencias con aminoácidos no estándar: **{quality['nonstd_aa_percentage']:.1f}%**
        - Secuencias de alta calidad: **{quality['high_quality_sequences']:,}**
        """)

# Instancia global del tracker
analytics_tracker = AnalyticsTracker()