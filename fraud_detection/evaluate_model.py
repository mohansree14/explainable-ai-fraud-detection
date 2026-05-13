
import json
import sys
import os
import time

# Add backend to path to import models
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.models.fraud_classification.model import fraud_classifier

def evaluate():
    data_path = 'backend/data/evaluation_set.json'
    
    if not os.path.exists(data_path):
        print(f"Data file not found at {data_path}")
        return

    with open(data_path, 'r') as f:
        data = json.load(f)

    print(f"Loading {len(data)} examples for evaluation...")
    
    correct = 0
    total = len(data)
    
    results = []

    print("-" * 60)
    print(f"{'Text (Truncated)':<30} | {'Predicted':<20} | {'Actual':<15} | {'Result'}")
    print("-" * 60)

    for item in data:
        text = item["text"]
        true_label = item["label"]
        
        # Run prediction
        start_time = time.time()
        prediction = fraud_classifier.classify_fraud(text, "text")
        latency = (time.time() - start_time) * 1000
        
        predicted_label = prediction["fraud_type"]
        confidence = prediction["confidence"]
        
        # Simple accuracy check: 
        # For scams, we check if it detected *mostly* the right category or at least flagged it as a scam/suspicious if specific type mismatches.
        # For legitimate, it must be "Unknown" or low confidence.
        
        is_correct = False
        if true_label == "Legitimate":
            if predicted_label == "Unknown" or confidence < 0.5:
                is_correct = True
        else:
            # If it's a scam, any high confidence detection is "good" for binary detection,
            # but ideally we want specific class match.
            if predicted_label.lower() in true_label.lower() or true_label.lower() in predicted_label.lower():
                is_correct = True
            elif predicted_label == "Suspicious Message" and true_label != "Legitimate":
                is_correct = True # Partial credit/Acceptable for general catch-all

        if is_correct:
            correct += 1
        
        results.append({
            "text": text,
            "predicted": predicted_label,
            "actual": true_label,
            "correct": is_correct,
            "confidence": confidence,
            "latency_ms": latency
        })

        status = "✅ PASS" if is_correct else "❌ FAIL"
        print(f"{text[:27] + '...':<30} | {predicted_label:<20} | {true_label:<15} | {status}")

    accuracy = (correct / total) * 100
    avg_latency = sum(r["latency_ms"] for r in results) / total

    print("-" * 60)
    print(f"\nEvaluation Complete")
    print(f"Accuracy: {accuracy:.2f}% ({correct}/{total})")
    print(f"Average Latency: {avg_latency:.2f} ms")

if __name__ == "__main__":
    evaluate()
