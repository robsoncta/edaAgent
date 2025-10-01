from google.adk.agents import LlmAgent
from tools.data_analyzer import analyze_data
from tools.memory_manager import manage_memory

def data_explorer_agent(model):
    return LlmAgent(
        name="data_explorer",
        model=model,
        description="Especialista em análise estatística, executa cálculos, identifica padrões e detecta anomalias.",
        instruction="""
Você é especialista em exploração de dados.
Use data_analyzer para estatísticas, outliers, correlações, distribuições.
Armazene resultados importantes com manage_memory.
Responda com insights claros.
""",
        tools=[analyze_data, manage_memory]
    )