from fastapi import APIRouter, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import json
import sys
import os

from models.model_manager import model_manager

router = APIRouter()

class TrustScoreRequest(BaseModel):
    content: str
    content_type: str  # text, link, image, document
    metadata: Optional[dict] = None

class TrustScoreResponse(BaseModel):
    trust_score: int  # 0-100 scale
    risk_factors: List[str]
    recommendations: List[str]

@router.post("/trust", response_model=TrustScoreResponse)
async def calculate_trust_score(request: TrustScoreRequest):
    """
    Calculate a trust score for content on a 0-100 scale using the trust scoring model
    """
    # Call the trust scoring model through the model manager
    trust_score = model_manager.calculate_trust_score(request.content, request.content_type)
    
    # Generate risk factors and recommendations based on the score
    risk_factors = []
    recommendations = []
    
    if trust_score < 30:
        risk_factors.append("Low trust score indicates high risk")
        recommendations.append("Be extremely cautious with this content")
    elif trust_score < 50:
        risk_factors.append("Moderate trust score indicates some risk")
        recommendations.append("Verify the source before proceeding")
    else:
        risk_factors.append("High trust score indicates low risk")
        recommendations.append("Content appears to be trustworthy")
    
    # Add content-type specific recommendations
    if request.content_type == "link":
        recommendations.append("Check the URL domain carefully")
        recommendations.append("Look for HTTPS in the URL")
        recommendations.append("Hover over links to see the destination")
    elif request.content_type == "text":
        recommendations.append("Review content for suspicious language or requests")
    
    return TrustScoreResponse(
        trust_score=trust_score,
        risk_factors=risk_factors,
        recommendations=recommendations
    )