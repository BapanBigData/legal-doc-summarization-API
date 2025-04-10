from fastapi import APIRouter, HTTPException
from app.services.s3_pdf_handler import extract_text_from_pdf_s3

router = APIRouter()

@router.post("/extract-pdf")
def extract_from_s3(payload: dict):
    try:
        key = payload.get("key")
        if not key:
            raise ValueError("Missing file key.")

        extracted_text = extract_text_from_pdf_s3(key)
        return {"extracted_text": extracted_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
