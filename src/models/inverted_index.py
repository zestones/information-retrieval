import json
import time


class InvertedIndex:
    def __init__(self, document_parser):
        self.document_parser = document_parser

        # A dictionary with the term as key and a list of document numbers as value
        # ex: {'term': ['doc1', 'doc2']}
        self.IDX = {}

        self.TF = {}
        self.indexing_time = 0

    def construct_inverted_index(self) -> dict:
        """
        Constructs the inverted index and computes statistics.
        """
        term_frequencies = {}
        index = {}

        self.document_parser.parse_documents()

        start_time = time.time()
        for doc in self.document_parser.parsed_documents:
            docno = list(doc.keys())[0]
            tokens = list(doc.values())[0]

            for token in tokens:
                if token not in index:
                    index[token] = {docno}
                    term_frequencies[token] = {docno: 1}
                else:
                    index[token].add(docno)
                    term_frequencies.setdefault(token, {}).setdefault(docno, 0)
                    term_frequencies[token][docno] += 1
        end_time = time.time()

        self.indexing_time = end_time - start_time
        self.IDX = index
        self.TF = term_frequencies

    def export_inverted_index(self, filename: str) -> None:
        """
        Exports the inverted index to a JSON file.
        """
        inverted_index_data = {
            "inverted_index": self.IDX,
            "term_frequencies": self.TF,
            "parsed_documents": self.document_parser.parsed_documents,
        }

        # Convert sets to lists for serialization
        inverted_index_data["inverted_index"] = {
            k: list(v) for k, v in inverted_index_data["inverted_index"].items()}
        inverted_index_data["term_frequencies"] = {
            k: {k2: v2 for k2, v2 in v.items()} for k, v in inverted_index_data["term_frequencies"].items()}

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
