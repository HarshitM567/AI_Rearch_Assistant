# AI Research Companion

The AI Research Companion is a multimodal assistant for researchers. It
helps summarize, search, and interact with research papers (PDFs,
diagrams, lecture transcripts) using Azure OpenAI GPT models.

------------------------------------------------------------------------

## 🚀 Features

-   Upload research PDFs
-   Extract text, sections, equations, and metadata
-   Store embeddings in FAISS vector DB
-   Retrieval-Augmented Generation (RAG) pipeline for Q&A
-   Summarization with Azure OpenAI GPT
-   Streamlit UI frontend + FastAPI backend
-   Dockerized for easy deployment

------------------------------------------------------------------------

## 🛠 Tech Stack

-   **Frontend:** Streamlit
-   **Backend:** FastAPI
-   **LLM + Embeddings:** Azure OpenAI (GPT-4, Embeddings)
-   **Vector Store:** FAISS
-   **PDF Parsing:** PyMuPDF, pdfplumber
-   **Deployment:** Docker, Docker Compose

------------------------------------------------------------------------

## 📂 Project Structure

    ai_research_companion/
    │── backend/
    │   ├── main.py          # FastAPI backend entry
    │   ├── rag_pipeline.py  # RAG logic with FAISS + Azure OpenAI
    │   ├── pdf_ingest.py    # PDF parsing and embedding
    │   ├── requirements.txt
    │   ├── Dockerfile
    │
    │── frontend/
    │   ├── app.py           # Streamlit UI
    │   ├── requirements.txt
    │   ├── Dockerfile
    │
    │── docker-compose.yml
    │── .env.example
    │── README.md

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1. Clone Repository

``` bash
git clone <your_repo_url>
cd ai_research_companion
```

### 2. Configure Environment

-   Copy `.env.example` to `.env`
-   Fill in your **Azure OpenAI credentials**:

```{=html}
<!-- -->
```
    AZURE_OPENAI_ENDPOINT=your-endpoint
    AZURE_OPENAI_API_KEY=your-key
    AZURE_OPENAI_API_VERSION=2023-05-15
    AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT=embedding-model

### 3. Run with Docker

``` bash
docker compose up --build
```

-   Backend runs on `http://localhost:8000`
-   Frontend runs on `http://localhost:8501`

### 4. Run Locally (Optional)

-   Start backend:

``` bash
cd backend
uvicorn main:app --reload
```

-   Start frontend:

``` bash
cd frontend
streamlit run app.py
```

------------------------------------------------------------------------

## 🔮 Future Enhancements

-   🎤 Azure Speech Integration (voice Q&A)
-   🖼 Figure extraction with CLIP
-   📚 Multi-PDF project organization
-   🔐 Authentication & rate limiting

------------------------------------------------------------------------

## 📌 Author

Built by Harshit Mittal as a **resume-boosting AI project** combining
Azure OpenAI, FastAPI, and Streamlit.
