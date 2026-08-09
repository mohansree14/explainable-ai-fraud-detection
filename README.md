# Guardian AI - Financial Fraud & Scam Advisor Chatbot

Guardian AI is a specialized chatbot designed to detect financial frauds and scams in text messages and images (e.g., screenshots of fake ads, phishing emails).

## Features
- **Text Analysis**: Detects scam keywords and patterns in text.
- **Image Analysis (OCR)**: Extracts text from images (Hindi/English) and analyzes it for fraud indicators.
- **Risk Scoring**: assigns a 0-100 risk score to analyzed content.
- **Modern UI**: Dark-mode, responsive React frontend.

## Tech Stack
- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TailwindCSS
- **ML/OCR**: EasyOCR, PyTorch (CPU)

## Prerequisites
- Python 3.9+
- Node.js 16+

## Setup & Run

### 1. Backend Setup
Navigate to the root directory:
```bash
# Create virtual environment
python -m venv env

# Activate environment
# Windows:
.\env\Scripts\activate
# Mac/Linux:
# source env/bin/activate

# Install dependencies (This may take a few minutes for PyTorch/OCR)
pip install -r requirements.txt
```

**Run the Backend server:**
```bash
cd backend
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.
Docs at `http://localhost:8000/docs`.

### 2. Frontend Setup
Open a new terminal and navigate to `frontend`:
```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
Open `http://localhost:5173` in your browser.

## Project Structure
```
Guardan AI/
├── homepage/           # Premium Marketing Site (React)
├── dashboard/          # Platform Dashboard (Static HTML/JS)
├── frontend/           # Analysis Chat Application (React)
├── backend/            # FastAPI Intelligence Services
├── fraud_detection/    # NLP & Machine Learning Models
└── data/               # Dataset storage
```

## Additional Apps

### Marketing Homepage
```bash
cd homepage/ui
npm install
npm run dev
```
Open `http://localhost:5173`.

### Analysis Dashboard
The dashboard is accessible via the "Launch Platform" button on the homepage or directly at `/dashboard/index.html`.

## Reproducibility
- All Python dependencies are pinned in `requirements.txt`.
- The OCR model (EasyOCR) will automatically download model weights on the first run.
- `app/core/config.py` defaults to CPU usage for maximum compatibility.