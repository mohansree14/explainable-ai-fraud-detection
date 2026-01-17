# API Integration Guide

## Overview

This guide explains how the GuardianAI API integrates all fraud detection models through a centralized model management system. Each API endpoint corresponds to a specific model, and all models are managed through a unified interface.

## Model Management Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   API Routers   │◄──►│  Model Manager   │◄──►│   AI/ML Models     │
└─────────────────┘    └──────────────────┘    └────────────────────┘
       │                        │                       │
       ▼                        ▼                       ▼
┌─────────────┐    ┌──────────────────┐    ┌────────────────────┐
│ Text        │    │ Centralized      │    │ Fraud              │
│ Analysis    │    │ Model Access     │    │ Classification     │
├─────────────┤    │ Point            │    ├────────────────────┤
│ Trust       │    │                  │    │ Trust              │
│ Scoring     │    │ Handles all      │    │ Scoring            │
├─────────────┤    │ model loading,   │    ├────────────────────┤
│ Document    │    │ initialization,  │    │ Document           │
│ Verification│    │ and routing      │    │ Authenticity       │
├─────────────┤    │                  │    ├────────────────────┤
│ Deepfake    │    │                  │    │ Deepfake           │
│ Detection   │    │                  │    │ Detection          │
├─────────────┤    │                  │    ├────────────────────┤
│ Explanation │    │                  │    │ Explanation        │
│ Generation  │    │                  │    │ Generator          │
└─────────────┘    └──────────────────┘    └────────────────────┘
```

## API Endpoints and Model Integration

### 1. Text Analysis (`/analyze/text`)

**Model Used**: Fraud Classification Model

**Integration Flow**:
1. API receives text content
2. Router calls `model_manager.classify_fraud()`
3. Model manager routes to `fraud_classifier.classify_fraud()`
4. Fraud classification model analyzes text and returns results
5. API returns formatted response

**Example Request**:
```json
{
  "text": "URGENT: Click here to verify your account immediately!",
  "context": "email"
}
```

**Example Response**:
```json
{
  "fraud_type": "Potential Phishing",
  "confidence": 0.85,
  "is_fraud": true,
  "details": {
    "phishing_indicators": ["click here", "verify", "account"],
    "scam_keywords": ["urgent"]
  }
}
```

### 2. Trust Scoring (`/score/trust`)

**Model Used**: Trust Scoring Model

**Integration Flow**:
1. API receives content and type
2. Router calls `model_manager.calculate_trust_score()`
3. Model manager routes to `trust_scorer.calculate_trust_score()`
4. Trust scoring model evaluates content and returns score
5. API generates risk factors and recommendations
6. API returns formatted response

**Example Request**:
```json
{
  "content": "URGENT: Click here to verify your account immediately!",
  "content_type": "text"
}
```

**Example Response**:
```json
{
  "trust_score": 25,
  "risk_factors": ["Low trust score indicates high risk"],
  "recommendations": [
    "Be extremely cautious with this content",
    "Review content for suspicious language or requests"
  ]
}
```

### 3. Document Verification (`/verify/document`)

**Model Used**: Document Authenticity Model

**Integration Flow**:
1. API receives document file upload
2. Router saves temporary file and calls `model_manager.verify_document()`
3. Model manager routes to `document_authenticator.verify_document()`
4. Document authenticity model analyzes file and returns results
5. API adds file type validation
6. API returns formatted response

**Example Request**:
```multipart/form-data
file: document.pdf
```

**Example Response**:
```json
{
  "is_authentic": true,
  "confidence": 0.95,
  "issues_found": [],
  "recommendations": [
    "Check for watermarks and official seals",
    "Verify logos and formatting"
  ]
}
```

### 4. Deepfake Detection (`/detect/deepfake`)

**Model Used**: Deepfake Detection Model

**Integration Flow**:
1. API receives media file upload
2. Router determines media type and saves temporary file
3. Router calls `model_manager.detect_deepfake()`
4. Model manager routes to `deepfake_detector.detect_deepfake()`
5. Deepfake detection model analyzes media and returns results
6. API adds file type validation
7. API returns formatted response

**Example Request**:
```multipart/form-data
file: image.jpg
```

**Example Response**:
```json
{
  "is_deepfake": false,
  "confidence": 0.95,
  "analysis_details": {
    "face_landmarks_consistency": "Good",
    "eye_blink_pattern": "Natural"
  },
  "recommendations": [
    "For more accurate results, upload high-resolution images"
  ]
}
```

### 5. Fraud Explanation (`/explain/fraud`)

**Model Used**: Explanation Generator Model

**Integration Flow**:
1. API receives fraud analysis data
2. Router calls `model_manager.generate_explanation()`
3. Model manager routes to `explanation_generator.generate_explanation()`
4. Explanation model generates human-readable explanation
5. API returns formatted response

**Example Request**:
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

**Example Response**:
```json
{
  "explanation": "This content was flagged as potential phishing based on indicators that suggest an attempt to steal personal information. Keywords detected: urgent. Phishing indicators found: click here, verify, account.",
  "key_indicators": [
    "Suspicious URLs",
    "Requests for login credentials"
  ],
  "severity_level": "high",
  "recommended_actions": [
    "Do not enter any personal information",
    "Do not click on any links or download attachments"
  ]
}
```

## Model Manager Implementation

The `ModelManager` class provides a centralized interface for all AI models:

```python
class ModelManager:
    def __init__(self):
        # Initialize all models
        self.fraud_classifier = fraud_classifier
        self.trust_scorer = trust_scorer
        self.document_authenticator = document_authenticator
        self.deepfake_detector = deepfake_detector
        self.explanation_generator = explanation_generator
    
    # Methods to access each model
    def classify_fraud(self, content, content_type)
    def calculate_trust_score(self, content, content_type)
    def verify_document(self, file_path, file_type)
    def detect_deepfake(self, file_path, media_type)
    def generate_explanation(self, fraud_type, analysis_data, trust_score)
```

## Benefits of This Architecture

1. **Centralized Model Management**: All models are accessed through a single interface
2. **Easy Model Replacement**: New models can be swapped in without changing API code
3. **Consistent Error Handling**: Unified approach to model errors and exceptions
4. **Scalability**: Models can be distributed across different servers or services
5. **Monitoring**: Centralized logging and performance tracking
6. **Maintainability**: Clear separation between API logic and model logic

## Adding New Models

To add a new model to the system:

1. Create a new model directory in `models/`
2. Implement the model class with appropriate methods
3. Add the model to `model_manager.py`
4. Create a new router in `backend/routers/`
5. Include the router in `backend/main.py`
6. Update API documentation

This architecture ensures that all models are properly integrated with the API and can be managed efficiently.