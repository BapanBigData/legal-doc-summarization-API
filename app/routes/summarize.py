from fastapi import APIRouter, HTTPException
from app.schemas.request_schema import SummarizationRequest
from app.services.pegasus_summary import summarize_text_pegasus
from app.services.bart_summary import summarize_text_bart

router = APIRouter()

@router.post("/summarize")
def summarize(request: SummarizationRequest):
    text = request.text
    model = request.model.lower()

    if model == "pegasus":
        summary = summarize_text_pegasus(text)
    elif model == "bart":
        summary = summarize_text_bart(text)
    else:
        raise HTTPException(status_code=400, detail="Invalid model")

    return {
        "model_used": model,
        "summary": summary
    }
