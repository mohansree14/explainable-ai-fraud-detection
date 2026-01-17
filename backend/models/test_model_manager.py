"""
Test the Model Manager
Verify that all models are properly integrated and accessible through the model manager.
"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.model_manager import model_manager

def test_model_manager():
    """Test that all models are accessible through the model manager"""
    
    print("Testing Model Manager Integration")
    print("=" * 40)
    
    # Test fraud classification model
    print("1. Testing Fraud Classification Model")
    fraud_result = model_manager.classify_fraud("URGENT: Click here to verify your account!", "text")
    print(f"   Result: {fraud_result}")
    print(f"   Fraud Type: {fraud_result['fraud_type']}")
    print(f"   Confidence: {fraud_result['confidence']}")
    print()
    
    # Test trust scoring model
    print("2. Testing Trust Scoring Model")
    trust_score = model_manager.calculate_trust_score("URGENT: Click here to verify your account!", "text")
    print(f"   Trust Score: {trust_score}")
    print()
    
    # Test document authenticity model
    print("3. Testing Document Authenticity Model")
    doc_result = model_manager.verify_document("test_file.jpg", "image")
    print(f"   Is Authentic: {doc_result['is_authentic']}")
    print(f"   Confidence: {doc_result['confidence']}")
    print()
    
    # Test deepfake detection model
    print("4. Testing Deepfake Detection Model")
    deepfake_result = model_manager.detect_deepfake("test_media.mp4", "video")
    print(f"   Is Deepfake: {deepfake_result['is_deepfake']}")
    print(f"   Confidence: {deepfake_result['confidence']}")
    print()
    
    # Test explanation generator
    print("5. Testing Explanation Generator")
    explanation_result = model_manager.generate_explanation(
        "Potential Phishing", 
        {"phishing_indicators": ["click here", "verify"], "scam_keywords": ["urgent"]}, 
        25
    )
    print(f"   Explanation: {explanation_result['explanation'][:50]}...")
    print(f"   Severity: {explanation_result['severity_level']}")
    print()
    
    print("All models successfully integrated with Model Manager!")

if __name__ == "__main__":
    test_model_manager()