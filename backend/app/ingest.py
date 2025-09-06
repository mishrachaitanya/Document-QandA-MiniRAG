import os
import orjson
from typing import List, Tuple
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from .utils import clean_text, split_text


DATA_DIR = os.getenv("DATA_DIR", "/data")
INDEX_PATH = os.path.join(DATA_DIR, "index.faiss")
META_PATH = os.path.join(DATA_DIR, "metadata.jsonl")
EMBED_MODEL = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


_model = None
_index = None
_dim = 384 # all-MiniLM-L6-v2 output size




def _ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)




def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model




def load_or_create_index():
    global _index
    if _index is not None:
        return _index
    _ensure_dirs()
    if os.path.exists(INDEX_PATH):
        _index = faiss.read_index(INDEX_PATH)
    else:
        _index = faiss.IndexFlatIP(_dim)
    return _index




def save_index(index):
    faiss.write_index(index, INDEX_PATH)




def append_metadata(records: List[dict]):
    with open(META_PATH, "ab") as f:
        for r in records:
            f.write(orjson.dumps(r) + b"\n")




def read_metadata() -> List[dict]:
    if not os.path.exists(META_PATH):
        return []
    with open(META_PATH, "rb") as f:
        return [orjson.loads(line) for line in f]




def embed_texts(texts: List[str]) -> np.ndarray:
    emb = get_embedder().encode(texts, normalize_embeddings=True)
    return np.array(emb).astype("float32")




def ingest_pdf(file_path: str, doc_id: str) -> int:
    reader = PdfReader(file_path)
    pages = []
    for i, p in enumerate(reader.pages):
        try:
            pages.append(clean_text(p.extract_text() or ""))
        except Exception:
            pages.append("")
    chunks = []
    for pi, page in enumerate(pages):
        for c in split_text(page):
            if c:
                chunks.append({
                "doc_id": doc_id,
                "page": pi + 1,
                "text": c,
                })
    texts = [c["text"] for c in chunks]
    if not texts:
        return 0
    embs = embed_texts(texts)


    index = load_or_create_index()
    index.add(embs)
    save_index(index)


    # Add metadata with vector positions
    base = index.ntotal - len(texts)
    for i, c in enumerate(chunks):
        c["vec_id"] = base + i
    append_metadata(chunks)
    return len(chunks)




def search(query: str, top_k: int = 4) -> List[Tuple[float, dict]]:
    index = load_or_create_index()
    if index.ntotal == 0:
        return []
    q = embed_texts([query])
    D, I = index.search(q, top_k)
    meta = read_metadata()
    out = []
    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue
        # FAISS is append-only, ids align with order added
        rec = next((m for m in meta if m.get("vec_id") == int(idx)), None)
        if rec:
            out.append((float(score), rec))
    return out