from manager.text_processor import TextProcessor
from manager.text_processor import SnowballTextProcessor
from manager.text_processor import NltkTextProcessor
from manager.text_processor import SpacyTextProcessor
from manager.text_processor import CustomTextProcessor

from models.statistics import Statistics
import time
import json
import math

from colorama import Fore, Style
import zipfile
import gzip
import io


"""
    This class represents a collection of documents.
    The class provides methods to read the documents from a file, 
    construct the inverted index, and calculate term frequencies.
"""


class Collection:
    def __init__(self, filename: str,
                 plot_statistics: bool = True,
                 import_collection: bool = False,
                 export_collection: bool = False,
                 export_statistics: bool = False,
                 ltn_weighting: bool = False,
                 ltc_weighting: bool = False
                 ):
        self.text_processor = CustomTextProcessor()

        self.filename = filename
        self.label = filename.split('/')[-1].split('.')[0]

        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = []

        # We store the indexing time for each collection
        self.indexing_time = 0

        # A dictionary with the term as key and a list of document numbers as value
        # ex: {'term': ['doc1', 'doc2']}
        self.inverted_index = {}
        self.weighted_index = {}

        # A dictionary with the term as key and a dictionary of document numbers and term frequencies as value
        # ex: {'term': {'doc1': 2, 'doc2': 1}}
        self.collection_frequencies = {}
        if (import_collection):
            print(f'Importing {self.label}...')
            self.import_inverted_index(f'../res/{self.label}.json')
        else:
            print(f'Indexing {self.label}...')
            self.construct_inverted_index()
            if export_collection:
                self.export_inverted_index(f'../res/{self.label}.json')

        self.collection_size = len(self.parsed_documents)

        if (ltn_weighting):
            print("Constructing weighted inverted index...")
            self.construct_smart_ltn_inverted_index()
        elif (ltc_weighting):
            print("Constructing weighted inverted index...")
            self.construct_smart_ltc_inverted_index()

        self.collection_statistics = Statistics(
            self, export_statistics=export_statistics, plot_statistics=plot_statistics)

    def parse_document(self) -> list:
        """
        Parses the document and save the result in a list.
        """
        parsed_documents = []
        if (self.filename.endswith('.gz')):
            with gzip.open(self.filename, 'rt', encoding='utf-8') as f:
                parsed_documents = self._parse_document_lines(f.readlines())
        elif self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                parsed_documents = []
                for file_name in zip_file.namelist():
                    with zip_file.open(file_name) as binary_file:
                        with io.TextIOWrapper(binary_file, encoding='utf-8') as f:
                            parsed_documents.extend(self._parse_document_lines(f.readlines()))
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                parsed_documents = self._parse_document_lines(f.readlines())

        return parsed_documents

    def _parse_document_lines(self, lines: str) -> list:
        """
        Parses the document lines and returns a list of dictionaries.
        """
        parsed_dictionary = []
        current_content = ''

        for line in lines:
            if '<doc><docno>' in line:
                docno = line.split('<doc><docno>')[1].split('</docno>')[0]
            elif '</doc>' in line:
                parsed_dictionary.append({docno: current_content})
                current_content = ''
            else:
                current_content += line

        return parsed_dictionary

    def document_frequency(self, term: str) -> int:
        """
        Returns the document frequency of a term.
        """
        return len(self.inverted_index.get(term, []))

    def term_frequency(self, docno: str, term: str) -> int:
        """
        Returns the term frequency of a term in a document.
        """
        return self.term_frequencies.get(term, {}).get(docno, 0)

    def tf_idf_weight(self, docno: str, term: str) -> float:
        """
        Returns the tf-idf weight of a term in a document.
        """
        tf = self.term_frequency(docno, term)
        df = self.document_frequency(term)
        return (1 + math.log(tf)) * math.log(self.collection_size / df)

    def length_normalization(self: dict) -> dict:
        """
        Returns the length normalization of a weighted index.
        """
        for term, postings in self.inverted_index.items():
            for docno in postings:
                if docno in self.weighted_index[term]:
                    # calculate the sum of squares of the weights of all terms in the document
                    sum_of_squares = sum([math.pow(self.weighted_index[term].get(docno, 0), 2)
                                          for term in self.weighted_index])

                    # divide the weight of each term in the document by the square root of the sum of squares
                    self.weighted_index[term][docno] /= math.sqrt(sum_of_squares)

        return self.weighted_index

    def calculate_collection_frequencies(self):
        """
        Calculate collection frequency of terms.
        """
        for term, postings in self.inverted_index.items():
            frequency = sum(self.term_frequency(docno, term) for docno in postings)
            self.collection_frequencies[term] = frequency

    def construct_smart_ltc_inverted_index(self) -> dict:
        """
        Constructs the weighted inverted index.
        """
        self.construct_smart_ltn_inverted_index()
        self.length_normalization()

    def construct_smart_ltn_inverted_index(self) -> dict:
        """
        Constructs the weighted inverted index.
        """
        for term, postings in self.inverted_index.items():
            self.weighted_index[term] = {}
            for docno in postings:
                self.weighted_index[term][docno] = self.tf_idf_weight(docno, term)

        # save self.weighted_index to json file
        with open(f'../res/{self.label}_weighted.json', 'w') as f:
            json.dump(self.weighted_index, f)
        return self.weighted_index

    def construct_inverted_index(self) -> dict:
        """
        Constructs the inverted index and computes statistics.
        """
        term_frequencies = {}
        index = {}

        self.pre_process_documents()

        start_time = time.time()
        for doc in self.parsed_documents:
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
        self.inverted_index = index
        self.term_frequencies = term_frequencies

    def pre_process_documents(self) -> None:
        """
        Pre-processes the documents.
        """
        parsed_documents = self.parse_document()
        for doc in parsed_documents:
            docno = list(doc.keys())[0]
            content = list(doc.values())[0]

            tokens = self.text_processor.pre_processing(content)
            self.parsed_documents.append({docno: tokens})

    def export_inverted_index(self, filename: str) -> None:
        """
        Exports the inverted index to a JSON file.
        """
        inverted_index_data = {
            "inverted_index": self.inverted_index,
            "term_frequencies": self.term_frequencies,
            "parsed_documents": self.parsed_documents,
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

            self.inverted_index = inverted_index_data["inverted_index"]
            end_time = time.time()

            self.term_frequencies = inverted_index_data["term_frequencies"]
            self.parsed_documents = inverted_index_data["parsed_documents"]
            self.indexing_time = end_time - start_time
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
            print("Please run the program without the '-i' option to generate the inverted index.")
        except Exception as e:
            print(f"An error occurred while importing the inverted index: {str(e)}")

    def print_title(self, text: str) -> None:
        """
        Prints a title.
        """
        print(Fore.BLUE + text + Style.RESET_ALL)
        print('-' * len(text))

    def display_inverted_index(self):
        """
        Displays the inverted index with a title indicating the document name.
        """
        self.print_title(f"\nInverted Index of '{self.filename}\n'")
        for term, docnos in self.inverted_index.items():
            docno_list = ', '.join(
                [f'{Fore.GREEN}{docno}{Style.RESET_ALL}' for docno in docnos])
            print(f"{term}: {docno_list}")
        print()

    def display_term_frequencies(self) -> None:
        """
        Displays the term frequencies.
        """
        self.print_title(f"Term Frequencies of '{self.filename}'")

        for term in self.term_frequencies:
            print(term, end=': ')
            for docno in self.term_frequencies[term]:
                print(Fore.GREEN + docno + Style.RESET_ALL
                      + '(' + str(self.term_frequencies[term][docno]) + ')', end=' ')
            print()

        print()
