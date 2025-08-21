from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil

from .models import IngestPDFResponse, QueryRequest, QueryResponse, SourceChunk
from .deps import store
from .services.pdf_ingest import ingest_pdf
from .services.rag_pipeline import answer_query

app = FastAPI(title="AI Research Companion Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ingest/pdf", response_model=IngestPDFResponse)
async def ingest_pdf_endpoint(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Please upload a PDF file")
    tmp_dir = Path("/tmp/uploads")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / file.filename
    with tmp_path.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    try:
        doc_id, count = ingest_pdf(tmp_path, store)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            tmp_path.unlink(missing_ok=True)
        except Exception:
            pass

    return IngestPDFResponse(doc_id=doc_id, chunks_indexed=count)

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(body: QueryRequest):
    answer, sources = answer_query(body.query, store, body.doc_id, body.top_k)
    return QueryResponse(answer=answer, sources=[SourceChunk(**s) for s in sources])
