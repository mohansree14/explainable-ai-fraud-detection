import easyocr
import numpy as np
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def __init__(self):
        # Initialize EasyOCR reader for English and Hindi (common in scan examples)
        try:
            self.reader = easyocr.Reader(['en', 'hi'], gpu=False) # Force CPU for now for broad compatibility
            logger.info("OCR Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load OCR Model: {e}")
            self.reader = None

    def extract_text_from_bytes(self, image_bytes: bytes) -> str:
        if not self.reader:
            return "Error: OCR Model not initialized."
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            image_np = np.array(image)
            
            # Detail=0 returns simple list of text
            results = self.reader.readtext(image_np, detail=0) 
            return " ".join(results)
        except Exception as e:
            logger.error(f"Error extracting text: {e}")
            return ""

# Global instance
ocr_service = OCRService()
