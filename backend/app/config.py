import os
from pathlib import Path

class Settings:
    AZURE_OPENAI_API_KEY: str = os.getenv("AZURE_OPENAI_API_KEY", "")
    AZURE_OPENAI_ENDPOINT: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_API_VERSION: str = os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15")
    AZURE_OPENAI_CHAT_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "")
    AZURE_OPENAI_EMB_DEPLOYMENT: str = os.getenv("AZURE_OPENAI_EMB_DEPLOYMENT", "")

    VECTORSTORE_DIR: Path = Path(os.getenv("VECTORSTORE_DIR", "/data/vectorstore")).resolve()
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 1200))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 200))
    max_completion_tokens: int = int(os.getenv("max_completion_tokens", 4096))

settings = Settings()
settings.VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
