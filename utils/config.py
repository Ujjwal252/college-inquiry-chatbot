import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")

INTENTS_FILE_PATH = os.path.join(DATA_DIR, "intents.json")
FAQ_FILE_PATH = os.path.join(DATA_DIR, "faq.csv")
COLLEGE_INFO_FILE_PATH = os.path.join(DATA_DIR, "college_info.json")

CLASSIFIER_MODEL_PATH = os.path.join(MODELS_DIR, "classifier.pkl")
VECTORIZER_MODEL_PATH = os.path.join(MODELS_DIR, "vectorizer.pkl")
TFIDF_MODEL_PATH = os.path.join(MODELS_DIR, "tfidf.pkl")

# NLP settings
CONFIDENCE_THRESHOLD = 0.35
MAX_SUGGESTIONS = 3

# UI settings
APP_TITLE = "College Inquiry Chatbot"
APP_ICON = "💬"
BOT_NAME = "CampusBot"
COLLEGE_NAME = "Your College Name"

# Model settings
TEST_SIZE = 0.2
RANDOM_STATE = 42
