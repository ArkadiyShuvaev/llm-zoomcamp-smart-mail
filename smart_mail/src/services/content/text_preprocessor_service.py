import string

class TextPreprocessorService:
    @staticmethod
    def preprocess_text(text: str) -> str:
        """ Preprocesses the input text by removing special characters, converting to lowercase, and removing leading and trailing whitespaces. """

        text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
        text = text.lower().strip()
        punctuations = string.punctuation
        for char in punctuations:
            text = text.replace(char, "")

        return text
