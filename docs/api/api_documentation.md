# API Documentation

## Overview

The GuardianAI API provides endpoints for fraud detection, trust scoring, document verification, deepfake detection, and fraud explanation services.

## Base URL

```
http://localhost:8000 (for local development)
https://api.guardianai.com (for production)
```

## Authentication

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

Error responses follow this format:
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

## Endpoints

### Text Analysis

#### POST /analyze/text

Analyze text for fraud indicators.

**Request:**
```json
{
  "text": "URGENT: Click here to verify your account immediately!",
  "context": "email"
}
```

**Response:**
```json
{
  "fraud_type": "Potential Phishing",
  "confidence": 0.85,
  "is_fraud": true,
  "details": {
    "phishing_indicators": ["click here", "verify", "account"],
    "scam_keywords": ["urgent"],
    "suspicious_patterns": []
  }
}
```

#### POST /analyze/link

Analyze a link for phishing or malicious content.

**Request:**
```json
{
  "url": "http://suspicious-website.com"
}
```

**Response:**
```json
{
  "url": "http://suspicious-website.com",
  "is_malicious": true,
  "risk_score": 0.8,
  "details": {
    "checked_databases": ["PhishTank", "Spamhaus", "Google Safe Browsing"],
    "matches_found": [".tk"]
  }
}
```

### Trust Scoring

#### POST /score/trust

Calculate a trust score for content on a 0-100 scale.

**Request:**
```json
{
  "content": "URGENT: Click here to verify your account immediately!",
  "content_type": "text",
  "metadata": {}
}
```

**Response:**
```json
{
  "trust_score": 25,
  "risk_factors": [
    "High risk keywords detected: urgent, click here, verify, account"
  ],
  "recommendations": [
    "Be extremely cautious with this content",
    "Verify the source through official channels"
  ]
}
```

### Document Verification

#### POST /verify/document

Verify the authenticity of a document.

**Request:**
```multipart/form-data
file: document.pdf
```

**Response:**
```json
{
  "is_authentic": true,
  "confidence": 0.95,
  "issues_found": [],
  "recommendations": [
    "Check for watermarks and official seals",
    "Verify logos and formatting",
    "Cross-reference with official sources"
  ]
}
```

#### POST /verify/image

Verify the authenticity of an image.

**Request:**
```multipart/form-data
file: image.jpg
```

**Response:**
```json
{
  "is_authentic": true,
  "confidence": 0.9,
  "issues_found": [],
  "recommendations": [
    "Check for signs of digital manipulation",
    "Look for inconsistent lighting or shadows",
    "Verify metadata if available"
  ]
}
```

### Deepfake Detection

#### POST /detect/deepfake

Detect if an image or video is a deepfake.

**Request:**
```multipart/form-data
file: media.mp4
```

**Response:**
```json
{
  "is_deepfake": false,
  "confidence": 0.95,
  "analysis_details": {
    "face_landmarks_consistency": "Good",
    "eye_blink_pattern": "Natural",
    "skin_texture_analysis": "Consistent",
    "lighting_consistency": "Good",
    "edge_artifacts": "None detected"
  },
  "recommendations": [
    "For more accurate results, upload high-resolution media",
    "Multiple angles improve detection accuracy",
    "Natural lighting conditions provide better analysis"
  ]
}
```

### Fraud Explanation

#### POST /explain/fraud

Provide a human-readable explanation for why content was flagged as fraud.

**Request:**
```json
{
  "fraud_type": "Potential Phishing",
  "analysis_data": {
    "phishing_indicators": ["click here", "verify", "account"],
    "scam_keywords": ["urgent"]
  },
  "trust_score": 25
}
```

**Response:**
```json
{
  "explanation": "This content was flagged as potential phishing based on indicators that suggest an attempt to steal personal information.",
  "key_indicators": [
    "Suspicious URLs",
    "Requests for login credentials",
    "Impersonation of trusted entities"
  ],
  "severity_level": "high",
  "recommended_actions": [
    "Do not enter any personal information",
    "Do not click on any links or download attachments",
    "Report this to the impersonated organization directly",
    "Delete this message immediately"
  ]
}
```

## Rate Limiting

To ensure fair usage and system stability, the API implements rate limiting:
- 100 requests per minute per user
- 1000 requests per hour per user

Exceeding these limits will result in a 429 (Too Many Requests) response.

## Versioning

The API version is included in the URL path:
```
/v1/analyze/text
```

## CORS Policy

The API allows cross-origin requests from all domains during development. In production, only approved domains are allowed.