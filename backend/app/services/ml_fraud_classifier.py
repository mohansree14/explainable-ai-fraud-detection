import logging
import os

import joblib

logger = logging.getLogger(__name__)

# ponytail: assumes a full repo checkout (ml/ is a sibling of backend/).
# Docker's build context for backend/ doesn't include ml/, so this path
# won't resolve in a container image until ml/model/ is added to that
# build context (or the model is bundled inside backend/ instead).
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
