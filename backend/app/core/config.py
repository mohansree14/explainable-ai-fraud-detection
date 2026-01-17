from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "Guardian AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Model Settings
    USE_GPU: bool = False # Default to CPU for reproducibility on standard machines
    
    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()
