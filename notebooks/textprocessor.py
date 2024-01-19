from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

from nltk.tokenize import word_tokenize
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

from colorama import Fore

import time
import re
import tabulate

"""
This class is responsible for processing the text.
The class provides methods to tokenize, normalize, stem, and remove stop words.
"""
STOP_WORDS_FILE = '../lib/data/practice_04/stop-words-english4.txt'
LOW_FREQ_WORDS_FILE = '../lib/processed_data/words_to_remove.txt'

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

    def remove_numbers(self, text: str) -> str:
        """
        Removes tokens containing numbers from the list of tokens.
        """
        return re.sub(r'\d+', '', text)

    def remove_punctuation(self, text: str) -> str:
        """
        Removes punctuation from the list of tokens using a regex.
        """
        return re.sub(r'[^\w\s]', '', text)

    def remove_uni_chars(self, text: str) -> str:
        """
        Removes single characters from the list of tokens using a regex.
        """
        return re.sub(r'\b\w\b', '', text)

    def remove_unicode(self, text: str) -> str:
        """
        Removes unicode characters from the list of text using a regex.
        """
        return re.sub(r'[^\x00-\x7F]+', '', text)

    def remove_empty(self, tokens: list) -> list:
        """
        Removes empty strings from the list of tokens.
        """
        return [token for token in tokens if token != '']
    
    def remove_outliers(self, tokens: list) -> list:
        """
        Removes outlier tokens from the list of tokens.
        Remove non-alphabetic tokens.
        Remove low frequency tokens.
        The outlier tokens are tokens with a length smaller or equal to 2 or larger than 30.
        """
        return tokens
                   
    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_uni_chars(text)
        text = self.remove_unicode(text)
        
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.remove_stop_words(tokens)
        tokens = self.stem(tokens)
        
        tokens = self.remove_outliers(tokens)
        tokens = self.remove_empty(tokens)

        return tokens

    def load_stopwords_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            stopwords = set(word.strip() for word in file)
        return stopwords
    
    def load_low_freq_words_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            words = set(word.strip() for word in file)
        return words

class ReferenceRearrangedTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)
        
    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_uni_chars(text)
        text = self.remove_unicode(text)
        
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.remove_stop_words(tokens)
        tokens = self.stem(tokens)
        
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
        return "stop" + str(len(self.stop_words)) + "_porter_ref_rearranged"


class ReferenceTextProcessor(TextProcessor):
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

        tokens = self.remove_stop_words(tokens)
        tokens = self.remove_punctuation(tokens)
        tokens = self.remove_numbers(tokens)

        tokens = self.remove_uni_chars(tokens)
        tokens = self.remove_unicode(tokens)
        tokens = self.remove_empty(tokens)

        return tokens
    
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

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "stop" + str(len(self.stop_words)) + "_porter_ref"


class CustomTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)
        self.words_to_remove = self.load_low_freq_words_from_file(LOW_FREQ_WORDS_FILE)

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using PorterStemmer.
        """
        return [self.stemmer.stem(token) for token in tokens]

    def remove_outliers(self, tokens: list) -> list:
        """
        Removes outlier tokens from the list of tokens.
        Remove non-alphabetic tokens.
        Remove low frequency tokens.
        The outlier tokens are tokens with a length smaller or equal to 2 or larger than 30.
        """
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if len(token) > 2 and len(token) < 30]
        tokens = [token for token in tokens if token not in self.words_to_remove]
        return tokens

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "stop" + str(len(self.stop_words)) + "_porter"


class CustomTextProcessorNoStem(TextProcessor):
    def __init__(self) -> None:
        self.stop_words = self.load_stopwords_from_file(STOP_WORDS_FILE)

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_uni_chars(text)
        text = self.remove_unicode(text)
        
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.remove_stop_words(tokens)
        
        tokens = self.remove_outliers(tokens)
        tokens = self.remove_empty(tokens)

        return tokens
    
    def remove_outliers(self, tokens: list) -> list:
        """
        Removes outlier tokens from the list of tokens.
        Remove non-alphabetic tokens.
        Remove low frequency tokens.
        The outlier tokens are tokens with a length smaller or equal to 2 or larger than 30.
        """
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if len(token) > 2 and len(token) < 30]
        return tokens

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "stop" + str(len(self.stop_words)) + "_nostem"


class CustomTextProcessorNoStop(TextProcessor):
    def __init__(self) -> None:
        self.stemmer = PorterStemmer()

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_uni_chars(text)
        text = self.remove_unicode(text)
        
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)
        
        tokens = self.remove_outliers(tokens)
        tokens = self.remove_empty(tokens)

        return tokens
    
    def remove_outliers(self, tokens: list) -> list:
        """
        Removes outlier tokens from the list of tokens.
        Remove non-alphabetic tokens.
        Remove low frequency tokens.
        The outlier tokens are tokens with a length smaller or equal to 2 or larger than 30.
        """
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if len(token) > 2 and len(token) < 30]
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
        text = self.remove_punctuation(text)
        text = self.remove_numbers(text)
        text = self.remove_uni_chars(text)
        text = self.remove_unicode(text)
        
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        
        tokens = self.remove_outliers(tokens)
        tokens = self.remove_empty(tokens)

        return tokens
    
    def remove_outliers(self, tokens: list) -> list:
        """
        Removes outlier tokens from the list of tokens.
        Remove non-alphabetic tokens.
        Remove low frequency tokens.
        The outlier tokens are tokens with a length smaller or equal to 2 or larger than 30.
        """
        tokens = [token for token in tokens if token.isalpha()]
        tokens = [token for token in tokens if len(token) > 2 and len(token) < 30]
        return tokens
    

    def get_text_processor_name(self):
        """
        Returns the name of the text processor.
        """
        return "nostop_nostem"
