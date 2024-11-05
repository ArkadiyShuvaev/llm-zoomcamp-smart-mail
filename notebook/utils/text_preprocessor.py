import re
import string
from nltk.corpus import stopwords


class TextPreprocessor:
    def __init__(self, stop_words_language: str = "german"):
        self.stop_words = set(stopwords.words(stop_words_language))

    def preprocess(self, text: str) -> str:
        # Remove extra spaces
        text = text.strip()

        # Remove punctuation (except for meaningful ones like apostrophes)
        text = text.translate(str.maketrans('', '', string.punctuation.replace("'", "")))

        # Lowercase the text
        text = text.lower()

        # Remove stopwords
        text = ' '.join([word for word in text.split() if word not in self.stop_words])

        # Remove digits
        text = re.sub(r'\d+', '', text)

        return text

    def preprocess_text(self, text: str, lowercase: bool = True) -> str:
        if lowercase:
            text = text.lower()

        # Remove special characters but keep spaces and German umlauts
        #text = re.sub(r'[^0-9a-zäöüß.,\s]', '', text, flags=re.IGNORECASE)

        # Remove extra whitespace
        text = ' '.join(text.split())

        text = ' '.join([word for word in text.split() if word not in self.stop_words])

        return text
