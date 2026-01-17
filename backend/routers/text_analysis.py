from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import json
import sys
import os

from models.model_manager import model_manager

router = APIRouter()

class TextAnalysisRequest(BaseModel):
    text: str
    context: Optional[str] = None

class TextAnalysisResponse(BaseModel):
    fraud_type: str
    confidence: float
    is_fraud: bool
    details: dict

@router.post("/text", response_model=TextAnalysisResponse)
async def analyze_text(request: TextAnalysisRequest):
    """
    Analyze text for fraud indicators using the fraud classification model
    """
    # Call the fraud classification model through the model manager
    result = model_manager.classify_fraud(request.text, "text")
    
    return TextAnalysisResponse(
        fraud_type=result["fraud_type"],
        confidence=result["confidence"],
        is_fraud=result["confidence"] > 0.5,  # Threshold for fraud detection
        details=result["details"]
    )

@router.post("/link")
async def analyze_link(url: str = Form(...)):
    """
    Analyze a link for phishing or malicious content
    """
    # This is a placeholder implementation
    # In a real implementation, this would check against databases like PhishTank
    
    result = {
        "url": url,
        "is_malicious": False,
        "risk_score": 0.0,
        "details": {
            "checked_databases": ["PhishTank", "Spamhaus", "Google Safe Browsing"],
            "matches_found": []
        }
    }
    
    # Simple domain-based detection (placeholder)
    suspicious_domains = [".tk", ".ml", ".ga", ".cf", "bit.ly", "tinyurl"]
    
    for domain in suspicious_domains:
        if domain in url:
            result["is_malicious"] = True
            result["risk_score"] = 0.8
            result["details"]["matches_found"].append(domain)
            break
    
    return result