from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

from nltk.tokenize import word_tokenize
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

from colorama import Fore

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
        return [token for token in tokens if token not in self.stop_words]

    def remove_numbers(self, tokens: list) -> list:
        """
        Removes tokens containing numbers from the list of tokens.
        """
        return [token for token in tokens if not re.search(r'\d', token)]

    def remove_punctuation(self, tokens: list) -> list:
        """
        Removes punctuation from the list of tokens using a regex.
        """
        return [re.sub(r'[^\w\s]', '', token) for token in tokens]

    def remove_uni_chars(self, tokens: list) -> list:
        """
        Removes single characters from the list of tokens using a regex.
        """
        return [re.sub(r'\b\w\b', '', token) for token in tokens]

    def remove_unicode(self, tokens: list) -> list:
        """
        Removes unicode characters from the list of tokens using a regex.
        """
        return [re.sub(r'[^\x00-\x7F]+', '', token) for token in tokens]

    def remove_empty(self, tokens: list) -> list:
        """
        Removes empty strings from the list of tokens.
        """
        return [token for token in tokens if token != '']

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)

        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_numbers(tokens)

        tokens = self.remove_uni_chars(tokens)
        tokens = self.remove_unicode(tokens)
        tokens = self.remove_empty(tokens)

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


class SnowballTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = SnowballStemmer('english')
        self.stop_words = set(stopwords.words('english'))

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using SnowballStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]


class SpacyTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.nlp = English()
        self.stop_words = STOP_WORDS

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using Spacy.
        """
        return [token.lemma_ for token in self.nlp(' '.join(tokens)) if not token.is_stop]


class CustomTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "stop" + str(len(self.stop_words)) + "_porter"


class CustomTextProcessorNoStem(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)

        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_numbers(tokens)

        tokens = self.remove_uni_chars(tokens)
        tokens = self.remove_unicode(tokens)
        tokens = self.remove_empty(tokens)

        return tokens

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "stop" + str(len(self.stop_words)) + "_nostem"


class CustomTextProcessorNoStop(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)

        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_numbers(tokens)

        tokens = self.remove_uni_chars(tokens)
        tokens = self.remove_unicode(tokens)
        tokens = self.remove_empty(tokens)

        return tokens

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "nostop_porter"


class CustomTextProcessorNoStopNoStem(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)

        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_numbers(tokens)

        tokens = self.remove_uni_chars(tokens)
        tokens = self.remove_unicode(tokens)
        tokens = self.remove_empty(tokens)

        return tokens

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "nostop_nostem"


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
