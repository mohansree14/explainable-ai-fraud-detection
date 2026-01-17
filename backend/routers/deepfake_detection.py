from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import json
import sys
import os

from models.model_manager import model_manager

router = APIRouter()

class DeepfakeDetectionResponse(BaseModel):
    is_deepfake: bool
    confidence: float
    analysis_details: dict
    recommendations: list

@router.post("/deepfake", response_model=DeepfakeDetectionResponse)
async def detect_deepfake(file: UploadFile = File(...)):
    """
    Detect if an image or video is a deepfake using the deepfake detection model
    """
    try:
        # Save the uploaded file temporarily
        # In a production environment, you would want to handle this more securely
        temp_file_path = f"temp_{file.filename}"
        
        # Save file to disk
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Reset file pointer for potential reuse
        await file.seek(0)
        
        # Determine media type based on file extension
        media_type = "image"
        if file.filename and any(ext in file.filename.lower() for ext in [".mp4", ".avi", ".mov"]):
            media_type = "video"
        
        # Add file type checking
        allowed_types = ["image/jpeg", "image/png", "video/mp4", "video/avi"]
        if file.content_type not in allowed_types:
            result = {
                "is_deepfake": False,
                "confidence": 0.1,
                "analysis_details": {
                    "error": f"Unsupported file type: {file.content_type}"
                },
                "recommendations": ["Upload a JPEG, PNG, MP4, or AVI file"]
            }
            return DeepfakeDetectionResponse(**result)
        
        # Call the deepfake detection model through the model manager
        result = model_manager.detect_deepfake(temp_file_path, media_type)
        
        # Clean up temporary file
        try:
            os.remove(temp_file_path)
        except:
            pass
        
        return DeepfakeDetectionResponse(
            is_deepfake=result["is_deepfake"],
            confidence=result["confidence"],
            analysis_details=result["analysis_details"],
            recommendations=result["recommendations"]
        )
    except Exception as e:
        # Clean up temporary file in case of error
        try:
            if 'temp_file_path' in locals():
                os.remove(temp_file_path)
        except:
            pass
            
        # Return error response
        error_result = {
            "is_deepfake": False,
            "confidence": 0.0,
            "analysis_details": {
                "error": f"Failed to process file: {str(e)}"
            },
            "recommendations": ["Try uploading a different file"]
        }
        return DeepfakeDetectionResponse(**error_result)