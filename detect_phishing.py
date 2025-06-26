import pickle
import argparse
import os
from train_model import preprocess_text
import database as db

MODELS_DIR = 'models'
MODEL_PATH = os.path.join(MODELS_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')

def load_model_and_vectorizer():
    """
    Load trained model and vectorizer from disk.
    """
    try:
        with open(MODEL_PATH, 'rb') as mf, open(VECTORIZER_PATH, 'rb') as vf:
            return pickle.load(mf), pickle.load(vf)
    except FileNotFoundError:
        print("Model or vectorizer not found. Run setup first.")
        return None, None

def classify_email(email_text, model, vectorizer):
    """
    Preprocess, vectorize, and classify email text.
    Returns ('Phishing'|'Legitimate', confidence).
    """
    processed = preprocess_text(email_text)
    vec = vectorizer.transform([processed]).toarray()
    pred = model.predict(vec)[0]
    probs = model.predict_proba(vec)[0]
    idx = list(model.classes_).index('spam' if pred == 'spam' else 'ham')
    label = 'Phishing' if pred == 'spam' else 'Legitimate'
    return label, probs[idx]

def main():
    parser = argparse.ArgumentParser(description="Detect phishing emails.")
    parser.add_argument("--email", type=str, required=True, help="Full email text to analyze.")
    args = parser.parse_args()

    model, vectorizer = load_model_and_vectorizer()
    if not model or not vectorizer:
        return

    prediction, confidence = classify_email(args.email, model, vectorizer)
    print(f"\n[RESULT] Prediction: {prediction}\n[CONFIDENCE] {confidence * 100:.2f}%")

    # Log result to database
    db.save_analysis_result(args.email, prediction, confidence)
    print(f"Analysis logged to {db.DATABASE_NAME}.")

if __name__ == "__main__":
    main()
