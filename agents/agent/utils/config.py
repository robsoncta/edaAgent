import os
from pydantic import BaseSettings

class Config(BaseSettings):
    groq_api_key: str
    openai_api_key: str
    groq_model: str = "llama-3.1-70b-versatile"
    openai_model: str = "gpt-4o-mini"
    max_file_size: int = 50
    temp_dir: str = "temp_files"

    class Config:
        env_file = ".env" if os.path.exists(".env") else None
        case_sensitive = False

    def __init__(self, **values):
        super().__init__(**values)
        if not self.env_file:
            self.groq_api_key = os.environ.get("GROQ_API_KEY")
            self.openai_api_key = os.environ.get("OPENAI_API_KEY")
            # etc.