import re


def clean_text(t: str) -> str:
    t = re.sub(r"\s+", " ", t)
    return t.strip()


# Simple recursive splitter


def split_text(text: str, chunk_size: int = 800, overlap: int = 120):
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(len(tokens), start + chunk_size)
        chunk = " ".join(tokens[start:end])
        chunks.append(chunk)
        if end == len(tokens):
            break
        start = max(0, end - overlap)
    return chunks