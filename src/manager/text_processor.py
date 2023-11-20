from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

from nltk.tokenize import word_tokenize
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

import re


"""
This class is responsible for processing the text.
The class provides methods to tokenize, normalize, stem, and remove stop words.
"""
STOP_WORDS_FILE = '../lib/data/practice_04/stop-words-english4.txt'


class TextProcessor:
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
        return tokens

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return tokens

    def remove_numbers(self, tokens: list) -> list:
        """
        Removes numbers and digits from the list of tokens.
        """
        return tokens

    def remove_punctuation(self, tokens: list) -> list:
        """
        Removes punctuation from the list of tokens.
        """
        return tokens

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)
        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_numbers(tokens)
        tokens = self.remove_punctuation(tokens)
        return tokens

    def load_stopwords_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            stopwords = set(word.strip() for word in file)
        return stopwords


class NltkTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = set(stopwords.words('english'))

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]


class SnowballTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using SnowballStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]


class SpacyTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.nlp = English()
        self.stop_words = STOP_WORDS

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using Spacy.
        """
        return [token.lemma_ for token in self.nlp(' '.join(tokens)) if not token.is_stop]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]


class CustomTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]

    def remove_numbers(self, tokens: list) -> list:
        """
        Removes numbers and digits from the list of tokens.
        """
        return [token for token in tokens if not re.match(r'^\d+(\.\d+)?$', token)]

    def remove_punctuation(self, tokens: list) -> list:
        """
        Removes punctuation from the list of tokens using a regex.
        """
        return [re.sub(r'[^\w\s]', '', token) for token in tokens]


class RegexTextProcessor(TextProcessor):
    def __init__(self):
        self.token_pattern = r'\b\w+\b'  # Default token pattern matches words
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = PorterStemmer()

    def stem(self, tokens):
        """
        Stems the tokens using SnowballStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def set_token_pattern(self, pattern):
        """
        Sets the token pattern.
        """
        self.token_pattern = pattern

    def tokenize(self, text):
        """
        Tokenizes the text using the token pattern.
        """
        return re.findall(self.token_pattern, text)

    def to_lowercase(self, tokens):
        """
        Converts the tokens to lowercase.
        """
        return [token.lower() for token in tokens]

    def remove_punctuation(self, tokens):
        """
        Removes punctuation from the list of tokens using a regex.
        """
        return [re.sub(r'[^\w\s]', '', token) for token in tokens]

    def remove_numbers(self, tokens):
        """
        Removes numbers and digits from the list of tokens.
        """
        return [token for token in tokens if not re.match(r'^\d+(\.\d+)?$', token)]

    def remove_stop_words(self, tokens):
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]
