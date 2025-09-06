import os
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import AskRequest, AskResponse
from .ingest import ingest_pdf, search
from .rag import make_context, call_ollama


DATA_DIR = os.getenv("DATA_DIR", "/data")


app = FastAPI(title="Mini-RAG API")
app.add_middleware(
CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Only PDF files are supported")
    os.makedirs(DATA_DIR, exist_ok=True)
    doc_id = str(uuid.uuid4())
    dest = os.path.join(DATA_DIR, f"{doc_id}.pdf")
    with open(dest, "wb") as f:
        f.write(await file.read())
    chunks = ingest_pdf(dest, doc_id)
    return {"doc_id": doc_id, "chunks": chunks}


@app.post("/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    results = search(req.query, top_k=req.top_k)
    context = make_context(results)
    if not context:
        return AskResponse(answer="I couldn't find relevant content in the uploaded documents.", sources=[])
    prompt = (
        "Answer using the context snippets below. Mention page numbers when relevant.\n\n"
        f"Question: {req.query}\n\nContext:\n{context}\n\nAnswer:"
    )
    answer = call_ollama(prompt)
    sources = [
        {"page": rec[1]["page"], "doc_id": rec[1]["doc_id"], "score": rec[0]}
        for rec in results
    ]
    return AskResponse(answer=answer, sources=sources)
