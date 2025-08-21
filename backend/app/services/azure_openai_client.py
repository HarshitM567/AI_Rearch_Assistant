from openai import AzureOpenAI
from ..config import settings

_client = AzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.AZURE_OPENAI_API_VERSION,
)

CHAT_DEPLOYMENT = settings.AZURE_OPENAI_CHAT_DEPLOYMENT
EMB_DEPLOYMENT = settings.AZURE_OPENAI_EMB_DEPLOYMENT

def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = _client.embeddings.create(input=texts, model=EMB_DEPLOYMENT)
    return [d.embedding for d in resp.data]

def chat_complete(system_prompt: str, messages: list[dict], max_tokens: int = 512) -> str:
    resp = _client.chat.completions.create(
        model=CHAT_DEPLOYMENT,
        messages=[{"role": "system", "content": system_prompt}] + messages,
        temperature=1,
        max_completion_tokens=max_tokens,
    )
    return resp.choices[0].message.content
