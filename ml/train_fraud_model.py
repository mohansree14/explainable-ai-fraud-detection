"""
Trains a binary fraud/scam text classifier (TF-IDF + Logistic Regression),
evaluates it against a held-out split plus Guardian AI's own labeled examples,
and saves the trained pipeline + metrics report.

Run: python ml/train_fraud_model.py

Dataset: UCI SMS Spam Collection (CC BY 4.0), 5,572 labeled SMS messages,
committed at data/raw/sms_spam_collection.csv. Original source:
  https://raw.githubusercontent.com/mohitgupta-1O1/Kaggle-SMS-Spam-Collection-Dataset-/master/spam.csv
"""

import json
import os

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SMS_DATASET_PATH = os.path.join(ROOT, "data", "raw", "sms_spam_collection.csv")
DOMAIN_EVAL_PATH = os.path.join(ROOT, "backend", "data", "evaluation_set.json")
MODEL_PATH = os.path.join(ROOT, "ml", "model", "fraud_classifier.joblib")
METRICS_PATH = os.path.join(ROOT, "ml", "model", "metrics.json")


def load_sms_dataset():
    df = pd.read_csv(SMS_DATASET_PATH, encoding="latin-1", usecols=["v1", "v2"])
    df.columns = ["label", "text"]
    df = df.drop_duplicates().dropna()
    df["y"] = (df["label"] == "spam").astype(int)
    return df


def load_domain_eval_set():
    with open(DOMAIN_EVAL_PATH, "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df["y"] = (df["label"] != "Legitimate").astype(int)
    return df


def score(y_true, y_pred, y_prob):
    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "confusion_matrix": confusion_matrix(y_true, y_pred).tolist(),
        "n_samples": int(len(y_true)),
    }


def main():
    sms = load_sms_dataset()
    assert len(sms) > 1000, "SMS dataset looks truncated"

    train_df, test_df = train_test_split(
        sms, test_size=0.2, stratify=sms["y"], random_state=42
    )

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, stop_words="english", sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)),
    ])
    pipeline.fit(train_df["text"], train_df["y"])

    test_prob = pipeline.predict_proba(test_df["text"])[:, 1]
    test_pred = pipeline.predict(test_df["text"])
    held_out_metrics = score(test_df["y"], test_pred, test_prob)

    domain = load_domain_eval_set()
    domain_prob = pipeline.predict_proba(domain["text"])[:, 1]
    domain_pred = pipeline.predict(domain["text"])
    domain_metrics = score(domain["y"], domain_pred, domain_prob)

    for m in (held_out_metrics, domain_metrics):
        for key in ("accuracy", "precision", "recall", "f1", "roc_auc"):
            assert 0.0 <= m[key] <= 1.0

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    report = {
        "model": "TF-IDF (1-2 gram) + Logistic Regression",
        "training_set": {
            "source": "UCI SMS Spam Collection (data/raw/sms_spam_collection.csv)",
            "n_train": int(len(train_df)),
            "n_test": int(len(test_df)),
        },
        "held_out_test_metrics": held_out_metrics,
        "domain_eval_metrics": domain_metrics,
        "domain_eval_note": (
            "backend/data/evaluation_set.json contains Guardian AI's own scam "
            "examples (delivery/romance/job/investment scams, phishing) not seen "
            "during training — this measures generalization beyond generic SMS spam."
        ),
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"\nSaved model to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")


if __name__ == "__main__":
    main()
