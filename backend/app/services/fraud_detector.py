import re

class FraudDetector:
    def __init__(self):
        # Simple keywords for MVP
        self.scam_keywords = {
            "investment": ["skyrocketing", "guaranteed return", "profit", "stock code", "insider", "ntpc", "share price target"],
            "phishing": ["click here", "verify your account", "urgent", "suspend", "bank"],
            "job": ["hiring", "work from home", "daily income", "no experience"]
        }

    def analyze_text(self, text: str) -> dict:
        text_lower = text.lower()
        detected_types = []
        risk_score = 0
        
        # Rule-based analysis
        for category, keywords in self.scam_keywords.items():
            matches = [k for k in keywords if k in text_lower]
            if matches:
                detected_types.append(category)
                risk_score += len(matches) * 20 # Arbitrary scoring
        
        risk_score = min(risk_score, 100) # Cap at 100
        
        is_fraud = risk_score > 30
        
        return {
            "is_fraud": is_fraud,
            "risk_score": risk_score,
            "detected_types": detected_types,
            "analysis": f"Detected potential scam triggers: {', '.join(detected_types)}" if is_fraud else "No obvious scam triggers detected."
        }

fraud_detector = FraudDetector()
