import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

class TextPreprocessor:
    def __init__(self, use_stemming=True, use_lemmatization=False):
        self.use_stemming = use_stemming
        self.use_lemmatization = use_lemmatization
        
        # Initialize NLTK tools
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Get English stopwords and remove question words
        self.stop_words = set(stopwords.words('english'))
        question_words = {'what', 'when', 'where', 'who', 'how', 'why', 'which'}
        self.stop_words -= question_words
    
    def clean_text(self, text):
        # Lowercase
        text = text.lower()
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text):
        return word_tokenize(text)
    
    def remove_stopwords(self, tokens):
        return [token for token in tokens if token not in self.stop_words]
    
    def stem(self, tokens):
        return [self.stemmer.stem(token) for token in tokens]
    
    def lemmatize(self, tokens):
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def process(self, text):
        # Full pipeline
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = self.remove_stopwords(tokens)
        
        if self.use_stemming:
            processed = self.stem(filtered)
        elif self.use_lemmatization:
            processed = self.lemmatize(filtered)
        else:
            processed = filtered
        
        # Rejoin as string
        return ' '.join(processed)
    
    def process_batch(self, texts):
        return [self.process(text) for text in texts]
    
    def get_pipeline_info(self):
        return {
            'use_stemming': self.use_stemming,
            'use_lemmatization': self.use_lemmatization
        }

if __name__ == "__main__":
    # Test with 5 sample college queries
    preprocessor = TextPreprocessor(use_stemming=True, use_lemmatization=False)
    
    sample_queries = [
        "What is the fee structure for engineering?",
        "How do I check my attendance online?",
        "When are the semester exams scheduled?",
        "Where can I find the library timings?",
        "Why do I need 75% attendance for exams?"
    ]
    
    print("Testing TextPreprocessor with sample queries:")
    print("=" * 50)
    
    for query in sample_queries:
        processed = preprocessor.process(query)
        print(f"Input:  {query}")
        print(f"Output: {processed}")
        print("-" * 30)
    
    print("Pipeline info:", preprocessor.get_pipeline_info())