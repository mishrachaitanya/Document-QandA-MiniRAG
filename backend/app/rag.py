import os
import requests
from typing import List, Tuple

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

PROMPT = (
"You are a helpful assistant. Answer the user's question strictly using the provided context. "
"If the answer isn't in the context, say you don't know.\n\n"
"# Question:\n{question}\n\n# Context:\n{context}\n\n"
)

def call_ollama(prompt: str) -> str:
    resp = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=120,
    )
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "")

def make_context(results: List[Tuple[float, dict]]) -> str:
    lines = []
    for score, rec in results:
        lines.append(f"(p.{rec['page']} score={score:.3f}) {rec['text']}")
    return "\n\n".join(lines)