"""
Document & Image Authenticity Model
Checks if documents/images are fake or tampered with.
"""

class DocumentAuthenticator:
    def __init__(self):
        """
        Initialize the document authenticity model.
        In a real implementation, this would load the trained model weights.
        """
        pass
    
    def verify_document(self, file_path, file_type="image"):
        """
        Verify the authenticity of a document or image.
        
        Args:
            file_path: Path to the document/image file
            file_type: Type of file ("image", "pdf", "document")
            
        Returns:
            dict: Verification results including authenticity and confidence
        """
        # Placeholder implementation
        # In a real implementation, this would use computer vision techniques
        
        result = {
            "is_authentic": True,
            "confidence": 0.95,
            "issues_found": [],
            "recommendations": []
        }
        
        # Simple file type checking (placeholder)
        if file_type == "image":
            try:
                from app.services.ocr_service import ocr_service
                from models.fraud_classification.model import fraud_classifier

                # Perform OCR using the shared service
                # The service handles initialization and errors
                extracted_text = ocr_service.extract_text_from_bytes(open(file_path, "rb").read())
                
                if "Error:" in extracted_text and not extracted_text.startswith("Error"): # Check if it's just an error message string return
                     pass # Logic to handle service error string if needed, currently it returns text or error string

                
                # Add extracted text to results for debugging/display
                result["extracted_text"] = extracted_text
                
                # Run Fraud Classification on the extracted text
                fraud_result = fraud_classifier.classify_fraud(extracted_text, "text")
                
                if fraud_result["confidence"] > 0.5:
                    result["is_authentic"] = False
                    result["confidence"] = fraud_result["confidence"]
                    result["issues_found"].append(f"Potential Fraud Detected: {fraud_result['fraud_type']}")
                    result["issues_found"].extend(fraud_result.get("details", {}).get("risk_factors", []))
                    
                    # Merge recommendations
                    scam_recs = ["Do not click any links", "Block the sender", "Report to official agency"]
                    result["recommendations"] = scam_recs + result["recommendations"]

                else:
                     result["recommendations"].extend([
                        "Check for signs of digital manipulation",
                        "Verify metadata if available"
                    ])

            except Exception as e:
                print(f"OCR Error: {e}")
                result["issues_found"].append("OCR Analysis failed or image too blurry")

        elif file_type == "pdf":
            result["recommendations"].extend([
                "Check for watermarks and official seals",
                "Verify logos and formatting",
                "Cross-reference with official sources"
            ])
        
        return result

# Singleton instance for the application
document_authenticator = DocumentAuthenticator()