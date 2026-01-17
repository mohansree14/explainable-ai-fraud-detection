from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import sys
import os

from models.model_manager import model_manager

router = APIRouter()

class ExplanationRequest(BaseModel):
    fraud_type: str
    analysis_data: Dict[str, Any]
    trust_score: int

class ExplanationResponse(BaseModel):
    explanation: str
    key_indicators: List[str]
    severity_level: str  # low, medium, high
    recommended_actions: List[str]

@router.post("/fraud", response_model=ExplanationResponse)
async def explain_fraud(request: ExplanationRequest):
    """
    Provide a human-readable explanation for why content was flagged as fraud using the explanation model
    """
    # Call the explanation model through the model manager
    result = model_manager.generate_explanation(
        request.fraud_type, 
        request.analysis_data, 
        request.trust_score
    )
    
    return ExplanationResponse(
        explanation=result["explanation"],
        key_indicators=result["key_indicators"],
        severity_level=result["severity_level"],
        recommended_actions=result["recommended_actions"]
    )