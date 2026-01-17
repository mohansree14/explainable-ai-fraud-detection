from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import text_analysis, trust_scoring, document_verification, deepfake_detection, explanation
from app.services.eval_service import eval_service

app = FastAPI(
    title="GuardianAI Fraud Prevention API",
    description="API for detecting and preventing online frauds and scams",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(text_analysis.router, prefix="/analyze", tags=["Text Analysis"])
app.include_router(trust_scoring.router, prefix="/score", tags=["Trust Scoring"])
app.include_router(document_verification.router, prefix="/verify", tags=["Document Verification"])
app.include_router(deepfake_detection.router, prefix="/detect", tags=["Deepfake Detection"])
app.include_router(explanation.router, prefix="/explain", tags=["Fraud Explanation"])

@app.get("/")
async def root():
    return {"message": "Welcome to GuardianAI Fraud Prevention API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/evaluate")
async def evaluate_system():
    return eval_service.evaluate_model()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)