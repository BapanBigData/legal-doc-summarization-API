from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.azure_blob_handler import upload_file_to_blob
import uuid

router = APIRouter()

@router.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    try:
        file_ext = file.filename.split(".")[-1]
        if file_ext.lower() != "pdf":
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")

        unique_filename = f"{uuid.uuid4()}.pdf"
        blob_key = upload_file_to_blob(file.file, unique_filename)

        return {"key": blob_key}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
