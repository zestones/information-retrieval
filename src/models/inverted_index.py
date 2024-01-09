from collections import defaultdict

from colorama import Fore, Style
import tabulate
import time
import json
import re

from models.document_parser import DocumentParser


class InvertedIndex(DocumentParser):
    def __init__(self, filename: str, text_processor, parser_granularity: list, is_bm25fr: bool = False, is_preprocessed=False):
        """
        Initializes the InvertedIndex class.

        Args:
            filename (str): The filename of the document.
            text_processor: The text processor object.
            parser_granularity (list): The granularity of the parser.
            is_bm25fr (bool, optional): Flag indicating whether to use BM25FR scoring. Defaults to False.
        """
        self.ARTICLE = './/article'
        self.QUERY_FILE = '../lib/data/practice_04/topics_M2DSC_7Q.txt'

        self.query_vocabulary = set()

        self.is_bm25fr = is_bm25fr
        self.filename = filename
        self.text_processor = text_processor
        self.is_preprocessed = is_preprocessed

        if (parser_granularity is None):
            self.parser_granularity = [self.ARTICLE]
        else:
            self.parser_granularity = parser_granularity

        self.IDX = {}   # The inverted index
        self.TF = {}    # The term frequencies
        self.DF = {}    # The document frequencies

        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = {}
        self.inverted_index = defaultdict(list)
        self.term_frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.document_frequencies = defaultdict(lambda: defaultdict(int))

        self.document_frequency_time = 0
        self.indexing_time = 0
        self.total_time = 0

    def construct_inverted_index(self) -> dict:
        """
        Constructs the inverted index.

        Returns:
            dict: The constructed inverted index.
        """
        self.total_time = time.time()
        print(Fore.CYAN + "> Granularity:", self.parser_granularity, Style.RESET_ALL) 
        self.parse_documents()

        start = time.time()
        self.compute_document_frequency()
        self.document_frequency_time = time.time() - start
        
        self.total_time = time.time() - self.total_time 

        self.indexing_time = self.inverted_index_time_processing
        self.IDX = self.inverted_index
        self.TF = self.term_frequencies
        self.DF = self.document_frequencies

        print(tabulate.tabulate([
            ['Parsed documents', self.parsed_documents_time_processing],
            ['Inverted index', self.inverted_index_time_processing],
            ['Documents frequency', self.document_frequency_time],
            ['Term Frequency', self.tf_time_processing],
            ['XPath retrieval', self.xpath_time_processing],
            ['Pre processing', self.clean_time_processing],
            ['Text extraction', self.extract_text_time_processing],
            ['Total Time', self.total_time]
        ]))
        
        print(Fore.YELLOW + "> Indexing time:", self.indexing_time, "seconds" + Style.RESET_ALL)
        print()
    
    def compute_document_frequency(self) -> int:
        for term, _ in self.inverted_index.items():
            for granularity in self.parser_granularity:
                tag = re.sub(r'\[\d+\]', '', granularity).split("/")[-1]
                self.document_frequencies[term][tag] = self._document_frequency(term, tag)

    def _document_frequency(self, term: str, tag_cibled: str) -> int:
        """
        Returns the document frequency of a term.
        The document frequency is the sum of the frequencies of the term in all documents.
        # ! We compute the df based on the xpath and not on the entire document
        # - TO COMPUTE THE df based on the xpath use this formula:
        # - df = len(self.inverted_index.IDX.get(term, {}).get(xpath, {}))
        """
        docno_set = set()
        for x_path, docno_list in self.inverted_index.get(term, {}).items():
            tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
            if tag == tag_cibled:
                docno_set.update(docno_list)

        return len(docno_set)

    def export_inverted_index(self, filename: str) -> None:
        """
        Exports the inverted index to a JSON file.

        Args:
            filename (str): The filename of the JSON file.
        """
        inverted_index_data = {
            "inverted_index": self.IDX,
            "term_frequencies": self.TF,
            "document_frequencies": self.DF,
            "parsed_documents": self.parsed_documents,
        }

        with open(filename, "w") as file:
            json.dump(inverted_index_data, file)

    def import_inverted_index(self, filename: str) -> None:
        """
        Imports the inverted index from a JSON file.

        Args:
            filename (str): The filename of the JSON file.
        """
        try:
            start_time = time.time()
            with open(filename, "r") as file:
                inverted_index_data = json.load(file)

            self.IDX = inverted_index_data["inverted_index"]
            end_time = time.time()

            self.TF = inverted_index_data["term_frequencies"]
            self.DF = inverted_index_data["document_frequencies"]

            self.parsed_documents = inverted_index_data["parsed_documents"]
            self.indexing_time = end_time - start_time
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            print("Please run the program without the '-i' option to generate the inverted index.")
        except Exception as e:
            print(f"An error occurred while importing the inverted index: {str(e)}")
