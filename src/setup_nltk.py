import nltk

RESOURCES = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "averaged_perceptron_tagger",
    "omw-1.4",
]


def download_resources():
    for resource in RESOURCES:
        nltk.download(resource)
        print(f"Downloaded {resource} successfully.")


if __name__ == "__main__":
    download_resources()
