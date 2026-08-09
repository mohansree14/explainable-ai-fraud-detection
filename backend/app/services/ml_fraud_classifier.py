import logging
import os

import joblib

logger = logging.getLogger(__name__)

# Resolves to <repo_root>/ml/model/fraud_classifier.joblib. The Docker image
# mirrors this layout under /app (see backend/Dockerfile + docker-compose.yml),
# so this path works both in a full local checkout and in the container.
_MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),
    "ml", "model", "fraud_classifier.joblib",
)


class MLFraudClassifier:
    def __init__(self):
        try:
            self.pipeline = joblib.load(_MODEL_PATH)
            logger.info("ML fraud classifier loaded from %s", _MODEL_PATH)
        except Exception as e:
            logger.error("Failed to load ML fraud classifier from %s: %s", _MODEL_PATH, e)
            self.pipeline = None

    def predict(self, text: str) -> dict:
        if self.pipeline is None:
            return {"is_fraud": False, "probability": 0.0}
        probability = float(self.pipeline.predict_proba([text])[0, 1])
        return {"is_fraud": probability >= 0.5, "probability": probability}


ml_fraud_classifier = MLFraudClassifier()
