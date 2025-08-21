from .azure_openai_client import embed_texts, chat_complete
from .vector_store import FaissStore
import numpy as np


SYS_PROMPT = (
"You are an AI research assistant. Answer using only the provided context. "
"Cite page numbers inline like (p. 3). If the answer is not in context, say you don't know."
)




def answer_query(query: str, store: FaissStore, doc_id: str | None, top_k: int = 5) -> tuple[str, list[dict]]:
    qvec = embed_texts([query])[0]
    import faiss
    qvec = np.array([qvec], dtype="float32")
    faiss.normalize_L2(qvec)


    # Search within specified doc or across all docs
    results = []
    if doc_id:
        results = store.search(doc_id, qvec, top_k)
    else:
        # naive: iterate all doc folders
        for d in store.base.iterdir():
            if not d.is_dir():
                continue
            results.extend(store.search(d.name, qvec, top_k))
        results = sorted(results, key=lambda x: x[1], reverse=True)[:top_k]


    context_blocks = []
    sources = []
    for meta, score in results:
        snippet = meta["text"][:1200]
        context_blocks.append(f"(p. {meta['page']})\n{snippet}")
        sources.append({
            "doc_id": meta["doc_id"],
            "chunk_id": meta["chunk_id"],
            "text": snippet,
            "score": float(score),
            "page": meta["page"],
        })


    context = "\n\n".join(context_blocks) if context_blocks else ""
    user_prompt = (
        f"Question: {query}\n\n"
        f"Context:\n{context}"
    )


    answer = chat_complete(
        system_prompt=SYS_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
        max_tokens=800,
    )


    return answer, sources