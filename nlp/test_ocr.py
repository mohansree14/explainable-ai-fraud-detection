
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    import easyocr
    print("EasyOCR imported successfully")
except ImportError as e:
    print(f"Failed to import easyocr: {e}")
    sys.exit(1)

try:
    reader = easyocr.Reader(['en'], gpu=False)
    print("EasyOCR Reader initialized successfully")
except Exception as e:
    print(f"Failed to initialize EasyOCR Reader: {e}")
    sys.exit(1)

print("OCR Test Passed")
