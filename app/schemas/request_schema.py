from pydantic import BaseModel

class SummarizationRequest(BaseModel):
    text: str
    model: str  # "pegasus" or "bart"
