from collections import defaultdict

import tabulate
import time
import json
import re

from models.document_parser import DocumentParser


class InvertedIndex(DocumentParser):
    def __init__(self, filename: str, text_processor, parser_granularity: list, is_bm25fr: bool = False):
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

        self.tag_pattern = re.compile(r'<[^>]+>')
        self.query_vocabulary = set()

        self.is_bm25fr = is_bm25fr
        self.filename = filename
        self.text_processor = text_processor

        if (parser_granularity is None):
            self.parser_granularity = [self.ARTICLE]
        else:
            self.parser_granularity = parser_granularity

        self.IDX = {}   # The inverted index
        self.TF = {}    # The term frequencies

        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = {}
        self.inverted_index = defaultdict(list)
        self.term_frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

        self.indexing_time = 0
        self.total_time = 0

    def construct_inverted_index(self) -> dict:
        """
        Constructs the inverted index.

        Returns:
            dict: The constructed inverted index.
        """
        self.total_time = time.time()
        self.parse_documents()
        self.total_time = time.time() - self.total_time

        self.indexing_time = self.inverted_index_time_processing
        self.IDX = self.inverted_index
        self.TF = self.term_frequencies

        print(tabulate.tabulate([
            ['parsed_documents_time_processing', self.parsed_documents_time_processing],
            ['inverted_index_time_processing', self.inverted_index_time_processing],
            ['xpath_time_processing', self.xpath_time_processing],
            ['clean_time_processing', self.clean_time_processing],
            ['tf_time_processing', self.tf_time_processing],
            ['extract_text_time_processing', self.extract_text_time_processing],
            ['xml_to_json_time_processing', self.xml_to_json_time_processing],
            ['Total Parse Time', self.total_time]
        ]))

    def export_inverted_index(self, filename: str) -> None:
        """
        Exports the inverted index to a JSON file.

        Args:
            filename (str): The filename of the JSON file.
        """
        inverted_index_data = {
            "inverted_index": self.IDX,
            "term_frequencies": self.TF,
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

            self.parsed_documents = inverted_index_data["parsed_documents"]
            self.indexing_time = end_time - start_time
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            print("Please run the program without the '-i' option to generate the inverted index.")
        except Exception as e:
            print(f"An error occurred while importing the inverted index: {str(e)}")
