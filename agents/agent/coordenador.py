from google.adk.agent import Agent 
from google.adk.tools import AgentTool
from agents.agent.agent.data_explorer import data_explorer_agent
from agents.agent.agent.visualization_expert import visualization_expert_agent
from tools.csv_loader import load_csv
from tools.data_analyzer import analyze_data
from tools.chart_generator import generate_chart
from tools.memory_manager import manage_memory

root_agent=LlmAgent(
        name="coordenador",
        model="gemini-2.5-pro",
        description="Orquestra o fluxo de análise, delega tasks para agentes especializados e consolida resultados.",
        instruction="""
Você é o agente coordenador para análise exploratória de dados.
Passos:
1. Identifique o tipo de request: carregamento, análise, visualização ou conclusão.
2. Delegue para o agente apropriado usando as tools.
3. Consolide os resultados em uma resposta clara e concisa.
Mantenha o contexto da sessão usando memory_manager.
Seja conciso em respostas.
""",
        tools=[
            AgentTool(data_explorer_agent(model)),
            AgentTool(visualization_expert_agent(model)),
            load_csv,
            analyze_data,
            generate_chart,
            manage_memory
        ]
    )