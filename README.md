# 📄 Mini-RAG (Retrieval-Augmented Generation) App

This is a minimal **Document Insights** application built with:

* ⚡ **FastAPI** backend (document ingestion, embeddings, search, RAG pipeline)
* 🎨 **Vue 3 + Vite** frontend (upload documents & ask questions)
* 🐳 **Docker Compose** for easy local setup

---

## 🚀 Features

* Upload **PDFs** and index them with FAISS
* Query documents with **semantic search**
* Uses **RAG (Retrieval-Augmented Generation)** to generate contextual answers
* Web frontend for interactive use
* Dockerized for simple deployment

---

## 📂 Project Structure

```
mini-rag-gke/
│
├── backend/              # FastAPI backend
│   ├── app/              # Core FastAPI app
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/             # Vue 3 + Vite frontend
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yaml   # Orchestrates frontend & backend
├── README.md             # This file
├── .gitignore
└── .env.example          # Example env vars
```

---

## ⚙️ Prerequisites

* [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
* Node.js (only if you want to run frontend locally, optional)

---

## 🛠️ Setup & Run

1. Clone the repo:

   ```bash
   git clone https://github.com/<your-username>/mini-rag-gke.git
   cd mini-rag-gke
   ```

2. Create `.env` file based on `.env.example`:

   ```bash
   cp .env.example .env
   ```

3. Start the app:

   ```bash
   docker-compose up --build
   ```

4. Open in browser:

   * Frontend: [http://localhost:8080](http://localhost:8080)
   * Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📝 API Endpoints

* `GET /healthz` → Health check
* `POST /upload` → Upload PDF
* `POST /ask` → Ask question about uploaded docs

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

---

