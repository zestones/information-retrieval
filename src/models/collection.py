from manager.text_processor import TextProcessor
from manager.text_processor import SnowballTextProcessor
from manager.text_processor import NltkTextProcessor
from manager.text_processor import SpacyTextProcessor
from manager.text_processor import CustomTextProcessor
from manager.text_processor import RegexTextProcessor

from weighting_strategies.ltn_weighting import LTNWeighting
from weighting_strategies.ltc_weighting import LTCWeighting
from weighting_strategies.bm25_weighting import BM25Weighting
from weighting_strategies.weighting_strategy import WeightingStrategy

from models.statistics import Statistics
from models.document_parser import DocumentParser
from models.inverted_index import InvertedIndex


import time
from colorama import Fore, Style


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
                 ltc_weighting: bool = False,
                 bm25_weighting: bool = False,
                 export_weighted_idx: bool = False,
                 parser_granularity: list = ['.//sec']
                ):
        
        self.text_processor = CustomTextProcessor()
        self.filename = filename

        # Init the DocumentParser with the filename and the text processor
        self.document_parser = DocumentParser(filename, self.text_processor, parser_granularity)
        self.inverted_index = InvertedIndex(self.document_parser)

        self.label = filename.split('/')[-1].split('.')[0]

        # A dictionary with the term as key and a dictionary of document numbers and term frequencies as value
        # ex: {'term': {'doc1': 2, 'doc2': 1}}
        self.collection_frequencies = {}
        if (import_collection):
            print(Fore.GREEN + f'Importing collection : {self.label}' + Style.RESET_ALL)
            self.inverted_index.import_inverted_index(f'../res/{self.label}.json')
        else:
            print(Fore.GREEN + f'Indexing collection : {self.label}' + Style.RESET_ALL)
            self.inverted_index.construct_inverted_index()
            if export_collection:
                self.inverted_index.export_inverted_index(f'../res/{self.label}.json')

        print(Fore.YELLOW + "> Indexing time:",
              self.inverted_index.indexing_time, "seconds" + Style.RESET_ALL)
        print()

        self.collection_size = len(self.document_parser.parsed_documents)
        self.statistics = Statistics(self, export_statistics=export_statistics)

        if (ltn_weighting):
            self.print_title("LTN weighting")
            self.weighted_index = LTNWeighting().calculate_weight(self)
        elif (ltc_weighting):
            self.print_title("LTC weighting")
            self.weighted_index = LTCWeighting().calculate_weight(self)
        elif (bm25_weighting):
            self.print_title("BM25 weighting")
            self.weighted_index = BM25Weighting().calculate_weight(self)

        if (export_weighted_idx):
            WeightingStrategy().export_weighted_index(
                self.weighted_index, f'../res/{self.label}_weighted.json')

    def document_frequency(self, term: str) -> int:
        """
        Returns the document frequency of a term.
        The document frequency is the sum of the frequencies of the term in all documents.
        """
        return len(self.inverted_index.IDX.get(term, []))

    def term_frequency(self, docno: str, term: str) -> int:
        """
        Returns the term frequency of a term in a document.
        """
        return self.inverted_index.TF.get(term, {}).get(docno, 0)

    def document_length(self, docno: str) -> int:
        """
        Returns the length of a document.
        """
        return self.statistics.documents_lengths.get(docno, 0)

    def calculate_collection_frequencies(self):
        """
        Calculate collection frequency of terms.
        """
        for term, postings in self.inverted_index.IDX.items():
            frequency = 0
            for entry in postings:
                docno_list = entry.get('docno', [])
                frequency += sum(self.term_frequency(docno, term) for docno in docno_list)
            self.collection_frequencies[term] = frequency

    # -------------------------------------------------
    # ----------------- DISPLAY -----------------------
    # -------------------------------------------------

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
        for term, docnos in self.inverted_index.IDX.items():
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
