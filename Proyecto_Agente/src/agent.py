import os
import pandas as pd
from langchain_huggingface import HuggingFaceEndpoint
from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from src.tools import search_protein_info, generate_length_histogram, get_amino_acid_composition_tool, get_hydrophobicity_scores_tool, get_q3_distribution_tool, get_q8_distribution_tool
from langchain.tools import Tool
from functools import partial

def create_tool_agent(df: pd.DataFrame):
    """
    Crea un agente de LangChain que puede utilizar herramientas (como búsqueda y EDA).
    """
    huggingface_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
    if not huggingface_api_token:
        raise ValueError("""No se encontró la API key de Hugging Face. 
Por favor, guárdala como una variable de entorno llamada HUGGINGFACEHUB_API_TOKEN.""")

    # Modelo LLM
    llm = HuggingFaceEndpoint(
        repo_id="google/flan-t5-large",
        max_length=512,
        temperature=0.7,
        huggingfacehub_api_token=huggingface_api_token
    )

    # Prompt de ReAct (Razonamiento y Acción)
    # Este prompt le indica al agente cómo usar las herramientas
    prompt = hub.pull("hwchase17/react")

    # Herramientas
    # Envolvemos la herramienta de histograma para que reciba el dataframe actual
    amino_acid_composition_tool_with_df = partial(get_amino_acid_composition_tool, dataframe=df)
    hydrophobicity_scores_tool_with_df = partial(get_hydrophobicity_scores_tool, dataframe=df)
    q3_distribution_tool_with_df = partial(get_q3_distribution_tool, dataframe=df)
    q8_distribution_tool_with_df = partial(get_q8_distribution_tool, dataframe=df)
    histogram_tool_with_df = partial(generate_length_histogram, dataframe=df)
    
    tools = [
        Tool(
            name="BusquedaWeb",
            func=search_protein_info,
            description="Busca información sobre una proteína o concepto biológico en Google. Útil para preguntas de conocimiento general."
        ),
        Tool(
            name="GeneradorHistogramaLongitud",
            func=histogram_tool_with_df,
            description="Genera un histograma de la longitud de las secuencias de proteínas. No necesita argumentos."
        )
        ,
        Tool(
            name="ComposicionAminoacidos",
            func=amino_acid_composition_tool_with_df,
            description="Calcula y devuelve la composición de aminoácidos del dataset. No necesita argumentos."
        ),
        Tool(
            name="ScoresHidrofobicidad",
            func=hydrophobicity_scores_tool_with_df,
            description="Calcula y devuelve los scores promedio de hidrofobicidad para cada secuencia. No necesita argumentos."
        ),
        Tool(
            name="DistribucionQ3",
            func=q3_distribution_tool_with_df,
            description="Devuelve la distribución de los estados secundarios Q3 del dataset. No necesita argumentos."
        ),
        Tool(
            name="DistribucionQ8",
            func=q8_distribution_tool_with_df,
            description="Devuelve la distribución de los estados secundarios Q8 del dataset. No necesita argumentos."
        )
    ]

    # Crear el agente
    agent = create_react_agent(llm, tools, prompt)

    # Crear el ejecutor del agente
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    return agent_executor
