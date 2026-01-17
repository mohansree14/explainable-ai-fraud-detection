"""
Fraud Classification Model
Detects the type of scam from text, images, or other content.
"""

class FraudClassifier:
    def __init__(self):
        """
        Initialize the fraud classification model.
        In a real implementation, this would load the trained model weights.
        """
        pass
    
    def classify_fraud(self, content, content_type="text"):
        """
        Classify the type of fraud in the given content.
        
        Args:
            content: The content to analyze (text, image, etc.)
            content_type: The type of content ("text", "image", "link")
            
        Returns:
            dict: Classification results including fraud type and confidence
        """
        # Placeholder implementation
        # In a real implementation, this would use a trained ML model
        
        result = {
            "fraud_type": "Unknown",
            "confidence": 0.0,
            "details": {}
        }
        
        if content_type == "text":
            # 1. Keyword-based classification
            scam_keywords = {
                "phishing": ["click here", "verify account", "login", "password", "update information", "verify identity", "suspended"],
                "fake_job": ["work from home", "no experience required", "urgent hiring"],
                "crypto_scam": ["bitcoin", "ethereum", "investment opportunity", "double your money"],
                "romance_scam": ["single", "looking for love", "far away", "military"],
                "delivery_scam": ["royal mail", "delivery", "parcel", "shipping", "failed attempt", "reschedule", "fee", "missed you", "bringing"]
            }
            
            content_lower = content.lower()
            detected_type = "Unknown"
            max_matches = 0
            risk_factors = []
            
            # 2. Heuristic Checks
            
            # Check for unprofessional tone/grammar
            if "failed to" in content_lower and ("royal mail" in content_lower or "delivery" in content_lower):
                risk_factors.append("Unprofessional phrasing ('failed to')")
            if "bringing" in content_lower and ("royal mail" in content_lower):
                 risk_factors.append("Suspicious typo/phrasing ('bringing')")
            
            # Check for suspicious links
            suspicious_domains = ["web.app", "bit.ly", "tinyurl.com", "is.gd"]
            for domain in suspicious_domains:
                if domain in content_lower:
                    risk_factors.append(f"Suspicious link domain detected: {domain}")
                    max_matches += 2 # Boost score
            
            # Check for Reply Bar artifact (One-way communication check)
            if "type a message" in content_lower or "text message" in content_lower:
                if "royal mail" in content_lower or "gov.uk" in content_lower or "nhs" in content_lower:
                     risk_factors.append("Reply bar detected in official channel (Government texts are one-way)")
                     max_matches += 3 # High risk
            
            # Check Sender ID (heuristic based on text proximity, simplistic for single string)
            # If we see a mobile number format at the start/top and then "Royal Mail"
            import re
            mobile_pattern = r"07\d{3}\s?\d{6}"
            if re.search(mobile_pattern, content) and ("royal mail" in content_lower or "gov" in content_lower):
                 risk_factors.append("Official agency name associated with mobile number")
                 max_matches += 3

            for fraud_type, keywords in scam_keywords.items():
                matches = [kw for kw in keywords if kw in content_lower]
                if len(matches) > max_matches: # Prioritize keyword matches if we haven't found higher risk heuristics yet, or add to them
                    max_matches = len(matches) + (len(risk_factors) * 2) # Weight risk factors heavily
                    detected_type = fraud_type
                    result["details"][f"{fraud_type}_keywords"] = matches

            # Force specific detection if heuristics triggered
            if risk_factors:
                 if detected_type == "Unknown": detected_type = "Suspicious Message"
                 if max_matches < 3: max_matches = 3 # Ensure minimum threshold

            if max_matches > 0:
                result["fraud_type"] = detected_type.capitalize().replace("_", " ")
                # Cap confidence at 0.99
                result["confidence"] = min(0.3 * max_matches, 0.99)
                result["details"]["risk_factors"] = risk_factors
        
        return result

# Singleton instance for the application
fraud_classifier = FraudClassifier()