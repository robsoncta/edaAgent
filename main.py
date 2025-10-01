from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.coordenador import coordenador_agent
from utils.config import Config

class EDASystem:
    def __init__(self, llm_provider: str, max_tokens: int, config: Config):
        self.config = config
        self.llm_provider = llm_provider
        self.max_tokens = max_tokens
        self.model = self.get_model()
        self.coordinator = coordenador_agent(self.model)
        self.session_service = InMemorySessionService()
        self.runner = Runner(agent=self.coordinator)
        self.current_dataset: pd.DataFrame = None
        self.user_id = "default_user"
        self.session_id = "default_session"

    def get_model(self):
        if self.llm_provider == "groq":
            return LiteLlm(model=self.config.groq_model)
        return LiteLlm(model=self.config.openai_model)

    async def analyze(self, question: str) -> str:
        response = await self.runner.call_agent_async(
            question,
            user_id=self.user_id,
            session_id=self.session_id
        )
        return response.content
