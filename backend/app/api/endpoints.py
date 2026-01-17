from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.ocr_service import ocr_service
from app.services.fraud_detector import fraud_detector
from app.services.eval_service import eval_service

router = APIRouter()

class AnalysisResponse(BaseModel):
    is_fraud: bool
    risk_score: int
    detected_types: List[str]
    analysis: str
    extracted_text: Optional[str] = None

class TextAnalysisRequest(BaseModel):
    text: str

@router.post("/analyze/text", response_model=AnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    result = fraud_detector.analyze_text(request.text)
    return AnalysisResponse(**result)

@router.post("/analyze/image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")
    
    contents = await file.read()
    
    # 1. Extract Text
    text = ocr_service.extract_text_from_bytes(contents)
    if not text:
        return AnalysisResponse(
            is_fraud=False, 
            risk_score=0, 
            detected_types=[], 
            analysis="No text could be extracted from the image.",
            extracted_text=""
        )
    
    # 2. Analyze extracted text
    result = fraud_detector.analyze_text(text)
    result["extracted_text"] = text
    
    return AnalysisResponse(**result)

@router.get("/evaluate")
async def evaluate_system():
    return eval_service.evaluate_model()
