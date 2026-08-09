import re

from app.services.ml_fraud_classifier import ml_fraud_classifier

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
        rule_is_fraud = risk_score > 30

        # ML model runs independently and can flag things the keyword list
        # misses (or vice versa) - combined with OR so either signal firing
        # is enough. See docs/models/fraud_classifier_report.md for why the
        # ML model alone isn't trusted as the sole signal yet.
        ml_result = ml_fraud_classifier.predict(text)
        if ml_result["is_fraud"] and "ml_model" not in detected_types:
            detected_types.append("ml_model")

        is_fraud = rule_is_fraud or ml_result["is_fraud"]
        risk_score = max(risk_score, round(ml_result["probability"] * 100))

        if detected_types:
            analysis = f"Detected potential scam triggers: {', '.join(detected_types)}"
        else:
            analysis = "No obvious scam triggers detected."

        return {
            "is_fraud": is_fraud,
            "risk_score": risk_score,
            "detected_types": detected_types,
            "analysis": analysis,
            "ml_probability": round(ml_result["probability"], 3),
        }

fraud_detector = FraudDetector()
