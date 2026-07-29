from pydantic_settings import BaseSettings
from functools import lru_cache
class ChatbotSettings(BaseSettings):
    vector_store_persist: str = "/app/chroma_data"
    collection_name: str = "knowledge_base"
    max_session_turns: int = 50
@lru_cache
def get_settings() -> ChatbotSettings:
    return ChatbotSettings()
