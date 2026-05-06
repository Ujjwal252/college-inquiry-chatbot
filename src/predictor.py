import json
import os
import random
from datetime import datetime

import joblib
import numpy as np

from src.preprocessor import TextPreprocessor
from utils.config import (
    CONFIDENCE_THRESHOLD,
    CLASSIFIER_MODEL_PATH,
    VECTORIZER_MODEL_PATH,
    TFIDF_MODEL_PATH,
    INTENTS_FILE_PATH,
)


class IntentPredictor:
    def __init__(self):
        missing = []
        for path in (CLASSIFIER_MODEL_PATH, VECTORIZER_MODEL_PATH, TFIDF_MODEL_PATH):
            if not os.path.exists(path):
                missing.append(path)

        if missing:
            raise FileNotFoundError(
                "Missing model files. Please run trainer.py first to generate: "
                + ", ".join(missing)
            )

        self.model = joblib.load(CLASSIFIER_MODEL_PATH)
        self.vectorizer = joblib.load(VECTORIZER_MODEL_PATH)
        self.label_encoder = joblib.load(TFIDF_MODEL_PATH)

        if not os.path.exists(INTENTS_FILE_PATH):
            raise FileNotFoundError(
                f"Missing intents file at {INTENTS_FILE_PATH}. Ensure data/intents.json exists."
            )

        with open(INTENTS_FILE_PATH, "r", encoding="utf-8") as f:
            self.intents_data = json.load(f)

        self.preprocessor = TextPreprocessor()

        # Map intent tag -> responses
        self.intent_to_responses = {
            intent["tag"]: intent.get("responses", [])
            for intent in self.intents_data.get("intents", [])
        }

    def _get_response(self, intent_tag: str) -> str:
        responses = self.intent_to_responses.get(intent_tag, [])
        if not responses:
            return "I’m sorry, I didn’t understand that."  # safe fallback
        return random.choice(responses)

    def get_all_intents(self):
        return [intent["tag"] for intent in self.intents_data.get("intents", [])]

    def predict(self, user_input: str):
        processed_input = self.preprocessor.process(user_input)
        X = self.vectorizer.transform([processed_input])

        # predict_proba expected to exist (LogisticRegression)
        proba = self.model.predict_proba(X)[0]

        top_idx = int(np.argmax(proba))
        top_confidence = float(proba[top_idx])
        top_intent = str(self.label_encoder.inverse_transform([top_idx])[0])

        if top_confidence < CONFIDENCE_THRESHOLD:
            predicted_intent = "unknown"
            predicted_confidence = top_confidence
        else:
            predicted_intent = top_intent
            predicted_confidence = top_confidence

        response = self._get_response(predicted_intent)

        # Top-3 suggestions from raw probabilities
        top3_indices = np.argsort(proba)[::-1][:3]
        top_3_suggestions = [
            {
                "intent": str(self.label_encoder.inverse_transform([int(i)])[0]),
                "confidence": float(proba[int(i)]),
            }
            for i in top3_indices
        ]

        return {
            "intent": predicted_intent,
            "confidence": predicted_confidence,
            "response": response,
            "processed_input": processed_input,
            "top_3_suggestions": top_3_suggestions,
        }


if __name__ == "__main__":
    predictor = IntentPredictor()

    sample_queries = [
        "Hi!",
        "What is the fee structure for CSE?",
        "When are the semester exams scheduled?",
        "How do I check my attendance on portal?",
        "Where can I find the library timings?",
        "asdkjhasdkjhasd1234 ??? gibberish",
    ]

    print("Testing IntentPredictor\n" + "=" * 40)
    for q in sample_queries:
        result = predictor.predict(q)
        print(f"Input: {q}")
        print(f"Processed: {result['processed_input']}")
        print(f"Intent: {result['intent']} | Confidence: {result['confidence']:.3f}")
        print(f"Response: {result['response']}")
        print("Top-3:", result["top_3_suggestions"])
        print("-" * 40)

