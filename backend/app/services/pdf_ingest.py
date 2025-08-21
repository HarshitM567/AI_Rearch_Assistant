from pathlib import Path
import fitz # PyMuPDF
from .azure_openai_client import embed_texts
from ..utils.text import clean_text, chunk_text
from .vector_store import FaissStore
import numpy as np


from ..config import settings




def ingest_pdf(path: Path, store: FaissStore, doc_id: str | None = None) -> tuple[str, int]:
    doc = fitz.open(str(path))
    # extract text with page numbers
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append({"page": i + 1, "text": clean_text(text)})


    # chunk across pages but retain page attribution
    chunk_records = []
    for p in pages:
        chunks = chunk_text(p["text"], settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
        for ci, ch in enumerate(chunks):
            chunk_records.append({
            "chunk_id": f"p{p['page']}_c{ci}",
            "text": ch,
            "page": p["page"],
            })


    texts = [c["text"] for c in chunk_records]
    if not texts:
        raise ValueError("No text extracted from PDF")


    embs = embed_texts(texts)
    dim = len(embs[0])


    import faiss, numpy as np
    index = faiss.IndexFlatIP(dim)
    mat = np.array(embs, dtype="float32")
    # normalize for cosine similarity via inner product
    faiss.normalize_L2(mat)
    index.add(mat)


    if not doc_id:
        doc_id = store.next_doc_id()


    meta = []
    for i, rec in enumerate(chunk_records):
        meta.append({
        "idx": i,
        "chunk_id": rec["chunk_id"],
        "page": rec["page"],
        "text": rec["text"],
        "doc_id": doc_id,
        })


    store.persist(doc_id, index, meta)
    return doc_id, len(chunk_records)