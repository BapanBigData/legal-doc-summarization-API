from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import extract_pdf, upload_pdf, summarize

app = FastAPI(
    title="Legal Text Summarization API",
    description="Backend API for legal document summarization using FastAPI",
    version="1.0.0",
)

# CORS settings – allow frontend (Streamlit) to communicate
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(upload_pdf.router, prefix="", tags=["Upload PDF"])
app.include_router(extract_pdf.router, prefix="", tags=["Extract PDF"])
app.include_router(summarize.router, prefix="", tags=["Summarization"])

@app.get("/")
def root():
    return {"message": "Legal Summarization API is running"}
