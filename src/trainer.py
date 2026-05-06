import json
import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score

from src.preprocessor import TextPreprocessor
from utils.config import *

class IntentModelTrainer:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), sublinear_tf=True)
        self.classifier = LogisticRegression(max_iter=1000)
        self.label_encoder = LabelEncoder()
    
    def load_intents(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        patterns = []
        tags = []
        
        for intent in data['intents']:
            if intent['tag'] != 'unknown':
                for pattern in intent['patterns']:
                    patterns.append(pattern)
                    tags.append(intent['tag'])
        
        print(f"Loaded {len(patterns)} patterns from {len(set(tags))} intents.")
        return patterns, tags
    
    def train(self, filepath):
        # Load intents
        patterns, tags = self.load_intents(filepath)
        
        # Preprocess patterns
        processed_patterns = self.preprocessor.process_batch(patterns)
        
        # Encode labels
        labels = self.label_encoder.fit_transform(tags)
        
        # TF-IDF transformation
        X = self.vectorizer.fit_transform(processed_patterns)
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, labels, test_size=TEST_SIZE, random_state=RANDOM_STATE
        )
        
        # Train classifier
        self.classifier.fit(X_train, y_train)
        
        # Evaluate on test set
        y_pred = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.3f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        
        # Cross-validation
        cv_scores = cross_val_score(self.classifier, X, labels, cv=5)
        print(f"Cross-validation scores: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        # Save model components
        self._save_model()
        print("Model trained and saved successfully.")
    
    def _save_model(self):
        joblib.dump(self.classifier, CLASSIFIER_MODEL_PATH)
        joblib.dump(self.vectorizer, VECTORIZER_MODEL_PATH)
        joblib.dump(self.label_encoder, TFIDF_MODEL_PATH)

if __name__ == "__main__":
    trainer = IntentModelTrainer()
    trainer.train(INTENTS_FILE_PATH)