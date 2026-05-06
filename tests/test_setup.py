import importlib
import sys

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

MODULES = [
    "streamlit",
    "pandas",
    "numpy",
    "nltk",
    "sklearn",
    "joblib",
]


def check_import(module_name):
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", None)
        print(f"{module_name}: imported successfully, version={version}")
        return True
    except Exception as exc:
        print(f"{module_name}: FAILED to import ({exc})")
        return False


def check_nltk_resources():
    passed = True
    try:
        tokens = word_tokenize("test")
        print(f"word_tokenize: OK -> {tokens}")
    except Exception as exc:
        print(f"word_tokenize: FAILED ({exc})")
        passed = False

    try:
        words = stopwords.words("english")
        print(f"stopwords.words: OK -> {len(words)} words loaded")
    except Exception as exc:
        print(f"stopwords.words: FAILED ({exc})")
        passed = False

    return passed


def run_checks():
    all_passed = True

    for module_name in MODULES:
        if not check_import(module_name):
            all_passed = False

    if not check_nltk_resources():
        all_passed = False

    if all_passed:
        print("\nALL TESTS PASSED")
        return 0
    print("\nSOME TESTS FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(run_checks())
