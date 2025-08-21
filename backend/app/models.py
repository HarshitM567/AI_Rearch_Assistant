from pydantic import BaseModel
from typing import List, Optional

class IngestPDFResponse(BaseModel):
    doc_id: str
    chunks_indexed: int

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    doc_id: Optional[str] = None

class SourceChunk(BaseModel):
    doc_id: str
    chunk_id: str
    text: str
    score: float
    page: int

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]
