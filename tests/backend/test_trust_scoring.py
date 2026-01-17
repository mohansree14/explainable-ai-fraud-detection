"""
Tests for the trust scoring router
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_calculate_trust_score():
    """Test the trust scoring endpoint"""
    request_data = {
        "content": "URGENT: Click here to verify your account immediately!",
        "content_type": "text",
        "metadata": {}
    }
    
    response = client.post("/score/trust", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert "trust_score" in data
    assert "risk_factors" in data
    assert "recommendations" in data
    
    # Check that the response has the expected structure
    assert isinstance(data["trust_score"], int)
    assert 0 <= data["trust_score"] <= 100
    assert isinstance(data["risk_factors"], list)
    assert isinstance(data["recommendations"], list)

def test_calculate_trust_score_link():
    """Test trust scoring for links"""
    request_data = {
        "content": "http://suspicious-site.com",
        "content_type": "link",
        "metadata": {}
    }
    
    response = client.post("/score/trust", json=request_data)
    
    assert response.status_code == 200
    data = response.json()
    
    # Should include link-specific recommendations
    assert any("URL" in rec for rec in data["recommendations"])

if __name__ == "__main__":
    pytest.main([__file__])