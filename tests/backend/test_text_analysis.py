"""
Tests for the text analysis router
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_analyze_text():
    """Test the text analysis endpoint"""
    request_data = {
        "text": "URGENT: Click here to verify your account immediately!",
        "context": "email"
    }
    
    response = client.post("/analyze/text", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "fraud_type" in data
    assert "confidence" in data
    assert "is_fraud" in data
    assert "details" in data
    
    # Check that the response has the expected structure
    assert isinstance(data["fraud_type"], str)
    assert isinstance(data["confidence"], float)
    assert isinstance(data["is_fraud"], bool)
    assert isinstance(data["details"], dict)

def test_analyze_link():
    """Test the link analysis endpoint"""
    request_data = {
        "url": "http://example-phishing-site.com"
    }
    
    response = client.post("/analyze/link", data=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "url" in data
    assert "is_malicious" in data
    assert "risk_score" in data
    assert "details" in data

def test_analyze_text_empty():
    """Test text analysis with empty text"""
    request_data = {
        "text": "",
        "context": "email"
    }
    
    response = client.post("/analyze/text", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should still return a valid response even with empty text
    assert "fraud_type" in data
    assert "confidence" in data
    assert "is_fraud" in data

if __name__ == "__main__":
    pytest.main([__file__])