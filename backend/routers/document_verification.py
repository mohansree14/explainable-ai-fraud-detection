from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import json
import sys
import os

from models.model_manager import model_manager

router = APIRouter()

class DocumentVerificationResponse(BaseModel):
    is_authentic: bool
    confidence: float
    issues_found: list
    recommendations: list

@router.post("/document", response_model=DocumentVerificationResponse)
async def verify_document(file: UploadFile = File(...)):
    """
    Verify the authenticity of a document using the document authenticity model
    """
    # Save the uploaded file temporarily
    # In a production environment, you would want to handle this more securely
    temp_file_path = f"temp_{file.filename}"
    
    # Call the document authenticity model through the model manager
    # For now, we'll use a placeholder since we don't have the actual file content
    result = model_manager.verify_document(temp_file_path, "document")
    
    # Add file type checking
    allowed_types = ["image/jpeg", "image/png", "application/pdf"]
    if file.content_type not in allowed_types:
        result["is_authentic"] = False
        result["confidence"] = 0.1
        result["issues_found"].append(f"Unsupported file type: {file.content_type}")
        result["recommendations"].append("Upload a JPEG, PNG, or PDF file")
    
    return DocumentVerificationResponse(
        is_authentic=result["is_authentic"],
        confidence=result["confidence"],
        issues_found=result["issues_found"],
        recommendations=result["recommendations"]
    )

@router.post("/image", response_model=DocumentVerificationResponse)
async def verify_image(file: UploadFile = File(...)):
    """
    Verify the authenticity of an image using the document authenticity model
    """
    # Save the uploaded file temporarily
    # In a production environment, you would want to handle this more securely
    temp_file_path = f"temp_{file.filename}"
    
    # Call the document authenticity model through the model manager for image verification
    result = model_manager.verify_document(temp_file_path, "image")
    
    # Add file type checking
    allowed_types = ["image/jpeg", "image/png"]
    if file.content_type not in allowed_types:
        result["is_authentic"] = False
        result["confidence"] = 0.2
        result["issues_found"].append(f"Unsupported image type: {file.content_type}")
        result["recommendations"].append("Upload a JPEG or PNG image")
    
    return DocumentVerificationResponse(
        is_authentic=result["is_authentic"],
        confidence=result["confidence"],
        issues_found=result["issues_found"],
        recommendations=result["recommendations"]
    )