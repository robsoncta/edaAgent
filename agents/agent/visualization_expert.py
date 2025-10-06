from google.adk.agents import LlmAgent
from tools.chart_generator import generate_chart
from tools.memory_manager import manage_memory

def visualization_expert_agent(model):
    return LlmAgent(
        name="visualization_expert",
        model=model,
        description="Seleciona e gera visualizações apropriadas, interpreta padrões visuais.",
        instruction="""
Você é especialista em visualizações.
Use generate_chart para criar histogramas, scatters, boxplots, heatmaps, bars baseados no contexto.
Armazene caminhos de imagens com manage_memory.
Descreva os insights das visualizações.
""",
        tools=[generate_chart, manage_memory]
    )