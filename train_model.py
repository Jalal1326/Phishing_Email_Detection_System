import pandas as pd
import nltk
import re
import pickle
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import os

DATASET_PATH = 'data/Phishing_Email.csv'
MODELS_DIR = 'models'
MODEL_PATH = os.path.join(MODELS_DIR, 'model.pkl')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')

# Ensure stopwords are downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

def preprocess_text(text):
    """Clean and stem a single email message."""
    if not isinstance(text, str):
        return ""
    stemmer = PorterStemmer()
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    words = text.split()
    return ' '.join(
        stemmer.stem(w) for w in words 
        if w not in set(stopwords.words('english'))
    )

def train_and_evaluate_model():
    """
    Load data, train RandomForest on TF-IDF features, evaluate, 
    and save the trained model plus vectorizer.
    """
    print("Loading dataset...")
    try:
        df = pd.read_csv(DATASET_PATH)
    except FileNotFoundError:
        print(f"Dataset not found at '{DATASET_PATH}'.")
        return
    
    df.dropna(inplace=True)
    df = df[['Email Text', 'Email Type']]
    df.columns = ['message', 'label']
    df['label'] = df['label'].map({'Phishing Email': 'spam', 'Safe Email': 'ham'})

    print("Preprocessing text...")
    df['processed_message'] = df['message'].apply(preprocess_text)

    print("Extracting TF-IDF features...")
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X = vectorizer.fit_transform(df['processed_message']).toarray()
    y = df['label']

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    print("Training RandomForest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print("\n--- Evaluation ---")
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred, labels=['ham', 'spam']))
    print("Classification Report:")
    print(classification_report(
        y_test, y_pred, target_names=['Legitimate (ham)', 'Phishing (spam)']
    ))

    print("\nSaving model and vectorizer...")
    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(MODEL_PATH, 'wb') as mf:
        pickle.dump(model, mf)
    print(f"Model saved to {MODEL_PATH}")
    with open(VECTORIZER_PATH, 'wb') as vf:
        pickle.dump(vectorizer, vf)
    print(f"Vectorizer saved to {VECTORIZER_PATH}")

if __name__ == "__main__":
    train_and_evaluate_model()
