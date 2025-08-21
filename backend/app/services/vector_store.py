import json
import uuid
from pathlib import Path
from typing import List, Tuple
import faiss
import numpy as np

from ..config import settings

class FaissStore:
    def __init__(self, base_dir: Path):
        self.base = base_dir
        self.base.mkdir(parents=True, exist_ok=True)

    def _doc_dir(self, doc_id: str) -> Path:
        d = self.base / doc_id
        d.mkdir(parents=True, exist_ok=True)
        return d

    def create_or_load(self, doc_id: str, dim: int) -> faiss.IndexFlatIP:
        idx_path = self._doc_dir(doc_id) / "index.faiss"
        if idx_path.exists():
            return faiss.read_index(str(idx_path))
        return faiss.IndexFlatIP(dim)

    def persist(self, doc_id: str, index: faiss.Index, meta: List[dict]):
        idx_path = self._doc_dir(doc_id) / "index.faiss"
        faiss.write_index(index, str(idx_path))
        with open(self._doc_dir(doc_id) / "meta.jsonl", "w", encoding="utf-8") as f:
            for m in meta:
                f.write(json.dumps(m, ensure_ascii=False) + "\n")

    def search(self, doc_id: str, qvec: np.ndarray, top_k: int) -> List[Tuple[dict, float]]:
        idx_path = self._doc_dir(doc_id) / "index.faiss"
        meta_path = self._doc_dir(doc_id) / "meta.jsonl"
        if not idx_path.exists() or not meta_path.exists():
            return []
        index = faiss.read_index(str(idx_path))
        D, I = index.search(qvec.astype('float32'), top_k)
        metas = [json.loads(line) for line in open(meta_path, encoding="utf-8").read().splitlines()]
        out = []
        for idx, score in zip(I[0], D[0]):
            if idx == -1:
                continue
            meta = metas[idx]
            out.append((meta, float(score)))
        return out

    def next_doc_id(self) -> str:
        return str(uuid.uuid4())
