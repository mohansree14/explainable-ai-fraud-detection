"""
Explanation Model
Generates human-readable explanations for fraud detection results.
"""

class ExplanationGenerator:
    def __init__(self):
        """
        Initialize the explanation generator.
        In a real implementation, this would load the trained model weights.
        """
        pass
    
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
        explanation = ""
        key_indicators = []
        severity_level = "low"
        recommended_actions = []
        
        if fraud_type.lower() == "potential scam":
            explanation = "This content was flagged as a potential scam based on keywords and language patterns commonly associated with fraudulent communications."
            key_indicators = ["Urgent language", "Requests for immediate action", "Suspicious offers"]
            severity_level = "medium"
            recommended_actions = [
                "Do not click on any links in this message",
                "Do not provide personal information",
                "Verify the source through official channels",
                "Report this to the appropriate authorities"
            ]
        elif fraud_type.lower() == "potential phishing":
            explanation = "This content was flagged as potential phishing based on indicators that suggest an attempt to steal personal information."
            key_indicators = ["Suspicious URLs", "Requests for login credentials", "Impersonation of trusted entities"]
            severity_level = "high"
            recommended_actions = [
                "Do not enter any personal information",
                "Do not click on any links or download attachments",
                "Report this to the impersonated organization directly",
                "Delete this message immediately"
            ]
        elif trust_score < 30:
            explanation = "This content received a low trust score based on multiple risk factors."
            key_indicators = ["Multiple suspicious elements detected", "High-risk keywords found"]
            severity_level = "high"
            recommended_actions = [
                "Exercise extreme caution",
                "Do not engage with this content",
                "Verify through alternative means",
                "Consider reporting to authorities"
            ]
        else:
            explanation = "This content was analyzed but no significant fraud indicators were found. However, always remain vigilant."
            key_indicators = ["No major red flags detected"]
            severity_level = "low"
            recommended_actions = [
                "Stay alert for potential subtle indicators",
                "Verify information through official channels if in doubt",
                "Report anything suspicious"
            ]
        
        # Enhance explanation with analysis data if available
        if analysis_data:
            if "scam_keywords" in analysis_data and analysis_data["scam_keywords"]:
                explanation += f" Keywords detected: {', '.join(analysis_data['scam_keywords'])}."
            if "phishing_indicators" in analysis_data and analysis_data["phishing_indicators"]:
                explanation += f" Phishing indicators found: {', '.join(analysis_data['phishing_indicators'])}."
        
        return {
            "explanation": explanation,
            "key_indicators": key_indicators,
            "severity_level": severity_level,
            "recommended_actions": recommended_actions
        }

# Singleton instance for the application
explanation_generator = ExplanationGenerator()