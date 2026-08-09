"""
Tests for the hybrid (rule-based + ML) fraud detector.
Run from backend/: python -m pytest ../tests/backend/test_fraud_detector.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "backend"))

from app.services.fraud_detector import fraud_detector


def test_known_scam_is_flagged():
    result = fraud_detector.analyze_text(
        "URGENT hiring! Work from home and earn 5000/day. No experience needed."
    )
    assert result["is_fraud"] is True
    assert 0.0 <= result["ml_probability"] <= 1.0


def test_legitimate_message_not_flagged():
    result = fraud_detector.analyze_text("Meeting confirmed for tomorrow at 10 AM. See you there.")
    assert result["is_fraud"] is False
    assert 0.0 <= result["ml_probability"] <= 1.0


def test_response_shape():
    result = fraud_detector.analyze_text("test message")
    for key in ("is_fraud", "risk_score", "detected_types", "analysis", "ml_probability"):
        assert key in result
    assert 0 <= result["risk_score"] <= 100


if __name__ == "__main__":
    test_known_scam_is_flagged()
    test_legitimate_message_not_flagged()
    test_response_shape()
    print("All fraud_detector tests passed.")
