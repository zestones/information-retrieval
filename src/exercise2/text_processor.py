from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize


"""
This class is responsible for processing the text.
The class provides methods to tokenize, normalize, stem, and remove stop words.
"""
class TextProcessor:
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))   
    
    def tokenize(self, text: str) -> list:
        """
        Tokenizes the text.
        """
        return word_tokenize(text)

    def normalize(self, tokens: list) -> list:
        """
        Normalizes the tokens. 
        """
        return [token.lower() for token in tokens]

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]

    def post_processing(self, text: str) -> list:
        """
        Performs post-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)
        tokens = self.remove_stop_words(tokens)
        return tokens
    
    
    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        return tokens
