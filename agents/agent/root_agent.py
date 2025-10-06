from google.adk.agents import Agent
from agents.agent.coordenador import CoordenadorAgent

root_agent = Agent(
    name="root_agent",
    description="Agente principal que orquestra os subagentes.",
    sub_agents=[CoordenadorAgent()],
)
