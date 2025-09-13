import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk

nltk.download('stopwords')

def preprocess_text(text):
    """
    PRÉ-PROCESSAMENTO NLP
    Etapas:
    1. Normalização (minúsculas)
    2. Limpeza (remove pontuação)
    3. Remoção de stopwords
    4. Stemming (redução a raiz)
    """
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    tokens = text.split()
    
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words]
    
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    
    return ' '.join(tokens)