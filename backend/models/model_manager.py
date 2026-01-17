"""
Model Manager
Centralized management of all AI models used in the GuardianAI system.
"""

import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.fraud_classification.model import fraud_classifier
from models.trust_scoring.model import trust_scorer
from models.document_authenticity.model import document_authenticator
from models.deepfake_detection.model import deepfake_detector
from models.explanation.model import explanation_generator

class ModelManager:
    """
    Centralized manager for all AI models in the GuardianAI system.
    Provides a unified interface for accessing and using all models.
    """
    
    def __init__(self):
        """
        Initialize the model manager with all available models.
        """
        self.fraud_classifier = fraud_classifier
        self.trust_scorer = trust_scorer
        self.document_authenticator = document_authenticator
        self.deepfake_detector = deepfake_detector
        self.explanation_generator = explanation_generator
    
    def classify_fraud(self, content: str, content_type: str = "text") -> dict:
        """
        Classify the type of fraud in the given content.
        
        Args:
            content: The content to analyze (text, image, etc.)
            content_type: The type of content ("text", "image", "link")
            
        Returns:
            dict: Classification results including fraud type and confidence
        """
        return self.fraud_classifier.classify_fraud(content, content_type)
    
    def calculate_trust_score(self, content: str, content_type: str = "text") -> int:
        """
        Calculate a trust score for the given content.
        
        Args:
            content: The content to analyze (text, image, etc.)
            content_type: The type of content ("text", "image", "link")
            
        Returns:
            int: Trust score from 0-100 (higher is more trustworthy)
        """
        return self.trust_scorer.calculate_trust_score(content, content_type)
    
    def verify_document(self, file_path: str, file_type: str = "image") -> dict:
        """
        Verify the authenticity of a document or image.
        
        Args:
            file_path: Path to the document/image file
            file_type: Type of file ("image", "pdf", "document")
            
        Returns:
            dict: Verification results including authenticity and confidence
        """
        return self.document_authenticator.verify_document(file_path, file_type)
    
    def detect_deepfake(self, file_path: str, media_type: str = "image") -> dict:
        """
        Detect if an image or video is a deepfake.
        
        Args:
            file_path: Path to the image/video file
            media_type: Type of media ("image", "video")
            
        Returns:
            dict: Detection results including deepfake probability and analysis details
        """
        return self.deepfake_detector.detect_deepfake(file_path, media_type)
    
    def generate_explanation(self, fraud_type: str, analysis_data: dict, trust_score: int) -> dict:
        """
        Generate a human-readable explanation for fraud detection results.
        
        Args:
            fraud_type: Type of fraud detected
            analysis_data: Detailed analysis data from other models
            trust_score: Trust score from the trust scoring model
            
        Returns:
            dict: Explanation with key indicators, severity, and recommendations
        """
        return self.explanation_generator.generate_explanation(fraud_type, analysis_data, trust_score)

# Singleton instance for the application
model_manager = ModelManager()