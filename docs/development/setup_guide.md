# Development Setup Guide

## Prerequisites

Before setting up the GuardianAI project, ensure you have the following installed:

1. Python 3.8 or higher
2. Node.js 14 or higher (for frontend development)
3. Flutter SDK (for mobile app development)
4. Git
5. Docker (optional, for containerization)
6. Virtual environment tool (venv or conda)

## Project Structure

```
guardian-ai/
├── backend/              # FastAPI backend services
├── frontend/             # User interfaces
│   ├── mobile/           # Flutter mobile app
│   └── web/              # React web app
├── models/               # AI/ML models
├── data/                 # Data processing and storage
├── docs/                 # Documentation
└── tests/                # Test suite
```

## Backend Setup

### 1. Create a Virtual Environment

```bash
cd backend
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the backend directory with the following variables:

```env
# Database configuration
DATABASE_URL=mongodb://localhost:27017/guardianai
# or for PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/guardianai

# JWT configuration
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Cloud service configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-west-2
```

### 4. Run the Backend

```bash
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 5. API Documentation

Once the backend is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Frontend Setup

### Web App (React)

1. Navigate to the web frontend directory:
```bash
cd frontend/web
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The web app will be available at `http://localhost:3000`

### Mobile App (Flutter)

1. Navigate to the mobile frontend directory:
```bash
cd frontend/mobile
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run
```

## Data Processing Setup

### 1. Install Additional Data Processing Dependencies

```bash
cd data
pip install pandas scikit-learn numpy
```

### 2. Run Data Collection Script

```bash
python data_collector.py
```

### 3. Process Collected Data

```bash
python data_processor.py
```

## Model Development Setup

### 1. Install Machine Learning Dependencies

```bash
cd models
pip install tensorflow torch transformers scikit-learn opencv-python
```

### 2. Model Training

Each model directory contains a `train.py` script for training:

```bash
cd models/fraud_classification
python train.py
```

## Testing

### Backend Testing

```bash
cd backend
python -m pytest tests/
```

### Frontend Testing

#### Web App
```bash
cd frontend/web
npm test
```

#### Mobile App
```bash
cd frontend/mobile
flutter test
```

## Development Workflow

1. **Branching Strategy**
   - Create feature branches from `develop`
   - Use descriptive branch names (e.g., `feature/fraud-detection-model`)
   - Submit pull requests to `develop` branch

2. **Code Style**
   - Follow PEP 8 for Python code
   - Use ESLint for JavaScript/React code
   - Use Flutter linting for Dart code

3. **Commit Messages**
   - Use conventional commit messages
   - Example: `feat: add fraud classification model`
   - Reference issues when applicable

4. **Documentation**
   - Update relevant documentation with each feature
   - Add docstrings to all functions and classes
   - Maintain README files in each directory

## Deployment

### Backend Deployment

1. Build Docker image:
```bash
cd backend
docker build -t guardianai-backend .
```

2. Run container:
```bash
docker run -p 8000:8000 guardianai-backend
```

### Frontend Deployment

#### Web App
```bash
cd frontend/web
npm run build
```

Deploy the `build` directory to your web server.

#### Mobile App
```bash
cd frontend/mobile
flutter build apk  # For Android
flutter build ios  # For iOS
```

## Troubleshooting

### Common Issues

1. **Python dependencies not installing**
   - Ensure you're in the correct virtual environment
   - Try upgrading pip: `pip install --upgrade pip`

2. **Backend not starting**
   - Check if the port is already in use
   - Verify all environment variables are set

3. **Frontend not connecting to backend**
   - Check if the backend is running
   - Verify CORS settings
   - Check API endpoint URLs

### Getting Help

- Check the documentation in the `docs/` directory
- Review existing issues on the project repository
- Contact the development team for support