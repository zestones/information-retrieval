from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, SnowballStemmer

from nltk.tokenize import word_tokenize
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

from gensim import corpora
from gensim.models.ldamodel import LdaModel


"""
This class is responsible for processing the text.
The class provides methods to tokenize, normalize, stem, and remove stop words.
"""


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

    def pre_processing(self, text: str) -> list:
        """
        Performs pre-processing on the text.
        """
        tokens = self.tokenize(text)
        tokens = self.normalize(tokens)
        tokens = self.stem(tokens)
        tokens = self.remove_stop_words(tokens)
        return tokens


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


class GensimTextProcessor(TextProcessor):
    def __init__(self) -> None:
        self.dictionary = None
        self.lda_model = None
        self.num_topics = 10
        self.stop_words = set(stopwords.words('english'))

    def stem(self, tokens: list) -> list:
        """
        Stems the tokens using Gensim.
        """
        self.dictionary = corpora.Dictionary([tokens])
        corpus = [self.dictionary.doc2bow(tokens)]
        self.lda_model = LdaModel(corpus, num_topics=self.num_topics, id2word=self.dictionary)
        topics = self.lda_model.show_topics(
            num_topics=self.num_topics,
            num_words=10,
            formatted=False
        )
        return [topic[0][1] for topic in topics]

    def remove_stop_words(self, tokens: list) -> list:
        """
        Removes the stop words from the tokens.
        """
        return [token for token in tokens if token not in self.stop_words]
