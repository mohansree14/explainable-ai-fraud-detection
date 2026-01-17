"""
Configuration settings for the GuardianAI project
"""

import os
from typing import Optional

class Config:
    # Project settings
    PROJECT_NAME = "GuardianAI Fraud Prevention Chatbot"
    VERSION = "1.0.0"
    DESCRIPTION = "AI-powered chatbot for detecting and preventing online frauds and scams"
    
    # Backend settings
    BACKEND_HOST = os.getenv("BACKEND_HOST", "0.0.0.0")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    
    # Database settings
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./guardianai.db")
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "guardianai_secret_key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
    
    # Cloud settings
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION = os.getenv("AWS_REGION", "us-west-2")
    
    # Model paths
    FRAUD_MODEL_PATH = os.getenv("FRAUD_MODEL_PATH", "models/fraud_classification/model.pkl")
    TRUST_MODEL_PATH = os.getenv("TRUST_MODEL_PATH", "models/trust_scoring/model.pkl")
    DOCUMENT_MODEL_PATH = os.getenv("DOCUMENT_MODEL_PATH", "models/document_authenticity/model.pkl")
    DEEPFAKE_MODEL_PATH = os.getenv("DEEPFAKE_MODEL_PATH", "models/deepfake_detection/model.pkl")
    
    # Data directories
    RAW_DATA_DIR = os.getenv("RAW_DATA_DIR", "data/raw")
    PROCESSED_DATA_DIR = os.getenv("PROCESSED_DATA_DIR", "data/processed")
    DATASETS_DIR = os.getenv("DATASETS_DIR", "data/datasets")
    
    # API settings
    API_V1_PREFIX = "/api/v1"
    
    # Frontend settings
    FRONTEND_WEB_URL = os.getenv("FRONTEND_WEB_URL", "http://localhost:3000")
    FRONTEND_MOBILE_URL = os.getenv("FRONTEND_MOBILE_URL", "http://localhost:3001")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/guardianai.log")

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = os.getenv("DEV_DATABASE_URL", "sqlite:///./guardianai_dev.db")

class ProductionConfig(Config):
    DEBUG = False
    DATABASE_URL = os.getenv("PROD_DATABASE_URL", "postgresql://user:password@localhost:5432/guardianai")

class TestingConfig(Config):
    TESTING = True
    DATABASE_URL = os.getenv("TEST_DATABASE_URL", "sqlite:///./guardianai_test.db")

# Configuration factory
def get_config(config_name: Optional[str] = None) -> Config:
    """
    Get the appropriate configuration based on the environment.
    
    Args:
        config_name: Name of the configuration to use (dev, prod, test)
        
    Returns:
        Configuration object
    """
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    if not config_name:
        config_name = os.getenv("GUARDIANAI_ENV", "development")
    
    return configs.get(config_name, DevelopmentConfig)()

# Export the default configuration
config = get_config()