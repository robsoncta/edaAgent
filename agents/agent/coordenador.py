"""Coordinator agent responsible for orchestrating specialised sub-agents."""

from __future__ import annotations

from agents.agent._adk_compat import AgentTool, LlmAgent
from agents.agent.data_explorer import data_explorer_agent
from agents.agent.visualization_expert import visualization_expert_agent
from agents.agent.tools.chart_generator import generate_chart
from agents.agent.tools.csv_loader import load_csv
from agents.agent.tools.data_analyzer import analyze_data
from agents.agent.tools.memory_manager import manage_memory

DEFAULT_MODEL = "gemini-2.5-pro"


def CoordenadorAgent(model: str = DEFAULT_MODEL) -> LlmAgent:
    """Factory that builds the coordinator agent instance."""

    explorer_agent = data_explorer_agent(model)
    viz_agent = visualization_expert_agent(model)

    tools = [
        AgentTool(explorer_agent),
        AgentTool(viz_agent),
        load_csv,
        analyze_data,
        generate_chart,
        manage_memory,
    ]

    instruction = """
Você é o agente coordenador para análise exploratória de dados.
Passos:
1. Identifique o tipo de request: carregamento, análise, visualização ou conclusão.
2. Delegue para o agente apropriado usando as tools.
3. Consolide os resultados em uma resposta clara e concisa.
Mantenha o contexto da sessão usando memory_manager.
Seja conciso em respostas.
""".strip()

    return LlmAgent(
        name="coordenador",
        model=model,
        description=(
            "Orquestra o fluxo de análise, delega tasks para agentes "
            "especializados e consolida resultados."
        ),
        instruction=instruction,
        tools=tools,
    )


__all__ = ["CoordenadorAgent", "DEFAULT_MODEL"]
