"""
Trust Scoring Model
Gives a 0-100 fraud risk score based on content analysis.
"""

class TrustScorer:
    def __init__(self):
        """
        Initialize the trust scoring model.
        In a real implementation, this would load the trained model weights.
        """
        pass
    
    def calculate_trust_score(self, content, content_type="text"):
        """
        Calculate a trust score for the given content.
        
        Args:
            content: The content to analyze (text, image, etc.)
            content_type: The type of content ("text", "image", "link")
            
        Returns:
            int: Trust score from 0-100 (higher is more trustworthy)
        """
        # Placeholder implementation
        # In a real implementation, this would use a trained ML model
        
        # Start with a neutral score
        trust_score = 50
        
        if content_type == "text":
            # Simple scoring based on keywords (placeholder)
            high_risk_keywords = ["urgent", "act now", "limited time", "click here", "verify immediately"]
            medium_risk_keywords = ["asap", "today only", "offer expires", "exclusive deal"]
            
            content_lower = content.lower()
            
            high_risk_matches = [word for word in high_risk_keywords if word in content_lower]
            medium_risk_matches = [word for word in medium_risk_keywords if word in content_lower]
            
            # Deduct points for risk factors
            trust_score -= min(10 * len(high_risk_matches), 30)
            trust_score -= min(5 * len(medium_risk_matches), 20)
            
            # Bonus for trust indicators
            trust_indicators = ["official", "verified", "certified", "guaranteed"]
            trust_matches = [word for word in trust_indicators if word in content_lower]
            trust_score += min(5 * len(trust_matches), 15)
        
        # Ensure score is within 0-100 range
        trust_score = max(0, min(100, trust_score))
        
        return trust_score

# Singleton instance for the application
trust_scorer = TrustScorer()