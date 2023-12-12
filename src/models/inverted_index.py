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
        term_frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        document_frequencies = defaultdict(int)
        index = defaultdict(list)

        parse_time = time.time()
        self.document_parser.parse_documents()
        parse_time = time.time() - parse_time

        print(f"> Parsing time: {parse_time} seconds")

        start_time = time.time()
        for docno, data in self.document_parser.parsed_documents.items():
            unique_x_paths = set()  # Store unique XPaths per document for faster checks

            for entry in data:
                x_path = entry["XPath"]
                terms = entry["terms"]

                if x_path not in unique_x_paths:
                    unique_x_paths.add(x_path)
                    document_frequencies[x_path] += 1

                    term_count = defaultdict(int)
                    for term in terms:
                        term_count[term] += 1

                    for term, count in term_count.items():
                        term_frequencies[term][x_path][docno] += count

                        # Update index if necessary
                        index_entry = next((e for e in index[term] if e["XPath"] == x_path), None)
                        if index_entry:
                            if docno not in index_entry["docno"]:
                                index_entry["docno"].append(docno)
                        else:
                            index[term].append({"XPath": x_path, "docno": [docno]})

        end_time = time.time()
        for term in index:
            index[term] = [entry for entry in index[term] if entry]

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
