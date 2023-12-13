import json
import time

from collections import defaultdict


class InvertedIndex:
    def __init__(self, document_parser):
        self.document_parser = document_parser

        # A dictionary with the term as key and a list of document numbers as value
        # ex: {'term': ['doc1', 'doc2']}
        self.IDX = {}

        # A dictionary with the term as key and a dictionary of document numbers and term frequencies as value
        # ex: {'term': {'doc1': 2, 'doc2': 1}}
        self.TF = {}
        self.indexing_time = 0

    def construct_inverted_index(self) -> dict:
        parse_time = time.time()
        self.document_parser.parse_documents()
        parse_time = time.time() - parse_time

        self.indexing_time = parse_time
        self.IDX = self.document_parser.inverted_index
        self.TF = self.document_parser.term_frequencies

    def export_inverted_index(self, filename: str) -> None:
        """
        Exports the inverted index to a JSON file.
        """
        inverted_index_data = {
            "inverted_index": self.IDX,
            "term_frequencies": self.TF,
            "parsed_documents": self.document_parser.parsed_documents,
        }

        with open(filename, "w") as file:
            json.dump(inverted_index_data, file)

    def import_inverted_index(self, filename: str) -> None:
        """
        Imports the inverted index from a JSON file.
        """
        try:
            start_time = time.time()
            with open(filename, "r") as file:
                inverted_index_data = json.load(file)

            self.IDX = inverted_index_data["inverted_index"]
            end_time = time.time()

            self.TF = inverted_index_data["term_frequencies"]

            self.document_parser.parsed_documents = inverted_index_data["parsed_documents"]
            self.indexing_time = end_time - start_time
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            print("Please run the program without the '-i' option to generate the inverted index.")
        except Exception as e:
            print(f"An error occurred while importing the inverted index: {str(e)}")
