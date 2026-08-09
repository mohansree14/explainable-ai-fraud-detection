# Guardian AI — Fraud Text Classifier: Model & Evaluation Report

**Date:** 2026-08-09
**Author:** Guardian AI engineering (drafted with Claude Code)
**Status:** For review — not yet integrated into the live API

## 1. Objective

The production system (`backend/app/services/fraud_detector.py`) is a
hand-written keyword matcher, not a trained model. This report documents a
first trained ML alternative: a binary text classifier that predicts
**fraud vs. legitimate** for a message, along with the dataset it was
trained on and its measured accuracy, precision, recall, F1, and ROC-AUC.

**Conclusion up front:** the model is strong on generic SMS spam but weak
on Guardian AI's actual target scams (see §5). It is not yet a drop-in
replacement for the rule-based detector.

## 2. Dataset

| | |
|---|---|
| Source | [UCI SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) |
| License | CC BY 4.0 |
| Location in repo | `data/raw/sms_spam_collection.csv` (gitignored per repo convention; re-download command is in `ml/train_fraud_model.py`) |
| Raw size | 5,574 SMS messages, labeled `ham` / `spam` |
| After cleaning | 5,169 messages (403 exact duplicates dropped, 0 missing values) |
| Class balance | 4,516 ham (legitimate) / 653 spam (fraud) — ~12.6% positive class |
| Split | 80% train (4,135) / 20% test (1,034), stratified by label, `random_state=42` |

A second, smaller set was used purely for **out-of-domain evaluation**, not
training:

| | |
|---|---|
| Source | `backend/data/evaluation_set.json` — Guardian AI's own hand-written scam examples |
| Size | 10 messages |
| Labels | Delivery Scam, Phishing, Fake Job, Romance Scam, Crypto Scam, Suspicious Message, Legitimate — collapsed to binary (`Legitimate` = 0, everything else = 1) for this evaluation |

## 3. Model

- **Type:** TF-IDF vectorizer (unigrams + bigrams, `min_df=2`, English stop
  words removed, sublinear TF scaling) feeding a Logistic Regression
  classifier (`class_weight="balanced"` to offset the ~1:7 class ratio).
- **Why this and not a neural net:** CPU-only, reproducible, fast to train
  (~2s), and a well-established strong baseline for short-text spam/fraud
  classification. Matches the project's existing CPU-only constraint (see
  README).
- **Training/eval code:** `ml/train_fraud_model.py`
- **Trained artifact:** `ml/model/fraud_classifier.joblib`
- **Raw metrics:** `ml/model/metrics.json`

## 4. Results

### 4.1 Held-out SMS test set (n = 1,034, same distribution as training data)

| Metric | Value |
|---|---|
| Accuracy | 97.7% |
| Precision | 0.928 |
| Recall | 0.885 |
| F1 | 0.906 |
| ROC-AUC | 0.993 |

Confusion matrix (rows = actual, columns = predicted; 0 = legitimate, 1 = fraud):

| | Pred: Legit | Pred: Fraud |
|---|---|---|
| **Actual: Legit** | 894 | 9 |
| **Actual: Fraud** | 15 | 116 |

### 4.2 Guardian AI domain eval set (n = 10, held out from training entirely)

| Metric | Value |
|---|---|
| Accuracy | 50.0% |
| Precision | 1.000 |
| Recall | 0.167 |
| F1 | 0.286 |
| ROC-AUC | 0.792 |

Confusion matrix:

| | Pred: Legit | Pred: Fraud |
|---|---|---|
| **Actual: Legit** | 4 | 0 |
| **Actual: Fraud** | 5 | 1 |

Per-example breakdown:

| Label | Actual | Predicted | Fraud prob. | Text |
|---|---|---|---|---|
| Delivery Scam | Fraud | **Legit (miss)** | 0.30 | "Your Royal Mail parcel was failed to deliver. Click here to reschedule: http://bit.ly/fake" |
| Suspicious Message | Fraud | Fraud (caught) | 0.69 | "Hi mum, I lost my phone. This is my new number 07123456789. Please message me on WhatsApp." |
| Fake Job | Fraud | **Legit (miss)** | 0.25 | "URGENT hiring! Work from home and earn 5000/day. No experience needed." |
| Phishing | Fraud | **Legit (miss)** | 0.39 | "Your account has been suspended. Verify identity now at secure-bank.web.app" |
| Romance Scam | Fraud | **Legit (miss)** | 0.15 | "Hey, are you still single? I am a military doctor currently deployed." |
| Crypto Scam | Fraud | **Legit (miss)** | 0.27 | "Bitcoin is skyrocketing! Invest now to double your money in 24 hours." |
| Legitimate | Legit | Legit (correct) | 0.22 | "Your package has been delivered to your neighbor at #42." |
| Legitimate | Legit | Legit (correct) | 0.21 | "Meeting confirmed for tomorrow at 10 AM. See you there." |
| Legitimate | Legit | Legit (correct) | 0.25 | "The project deadline is extended by two days." |
| Legitimate | Legit | Legit (correct) | 0.17 | "Royal Mail: We are bringing your parcel today between 2-4pm." |

## 5. Analysis

The model performs excellently in-distribution (97.7% accuracy, 0.99
ROC-AUC on held-out SMS spam) but misses 5 of 6 real scam examples in
Guardian AI's own domain set. It correctly rejected all 4 legitimate
messages (no false positives), so precision stayed perfect — the failure
mode is entirely **false negatives**.

**Root cause:** the UCI SMS Spam Collection is dominated by 2011-era UK
bulk-SMS advertising spam ("FREE", "WIN", "txt", "£", premium-rate
numbers). Guardian AI's target scams are social-engineering messages that
read like ordinary, well-written text — a fake delivery notice, a
"military doctor" romance opener, a bank-impersonation link — with none of
that bulk-spam vocabulary. The vectorizer simply never learned those
patterns.

**Caveats on the numbers themselves:**
- The domain eval set is only 10 examples — the 50%/0.79 figures are not
  statistically reliable on their own, but the failures are consistent
  with the root cause above, not noise.
- "Spam" (UCI's label) and "fraud" (this project's target) are related but
  not identical — some spam is unwanted marketing, not malicious.

## 6. Recommendation

Do not swap this model into the live API yet. To close the domain gap:

1. **Get real or realistic scam examples** — actual reported scam
   messages (anonymized) or a phishing/social-engineering-specific public
   corpus, layered on top of the current SMS spam data.
2. **Expand the domain eval set** well beyond 10 examples before trusting
   accuracy/recall numbers on it.
3. Re-train and re-evaluate with the same pipeline (`ml/train_fraud_model.py`
   already supports swapping in a larger dataset) before considering
   replacing `fraud_detector.py`.

## 7. Artifacts

| File | Purpose |
|---|---|
| `ml/train_fraud_model.py` | Training + evaluation pipeline (reproducible, `python ml/train_fraud_model.py`) |
| `ml/model/fraud_classifier.joblib` | Trained TF-IDF + Logistic Regression pipeline |
| `ml/model/metrics.json` | Machine-readable evaluation results |
| `ml/requirements.txt` | Training-only dependencies (scikit-learn, pandas, joblib) |
| `data/raw/sms_spam_collection.csv` | Training dataset (not committed; download command in training script) |
