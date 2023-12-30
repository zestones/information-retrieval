from manager.text_processor import TextProcessor
from manager.text_processor import SnowballTextProcessor
from manager.text_processor import NltkTextProcessor
from manager.text_processor import SpacyTextProcessor
from manager.text_processor import CustomTextProcessor
from manager.text_processor import RegexTextProcessor

from weighting_strategies.ltn_weighting import LTNWeighting
from weighting_strategies.ltc_weighting import LTCWeighting
from weighting_strategies.lnu_weighting import LNUWeighting
from weighting_strategies.bm25_weighting import BM25Weighting
from weighting_strategies.bm25Fw_weighting import BM25FwWeighting
from weighting_strategies.bm25Fr_weighting import BM25FrWeighting
from weighting_strategies.weighting_strategy import WeightingStrategy

from models.statistics import Statistics
from models.inverted_index import InvertedIndex

import json
import re

from colorama import Fore, Style


"""
    This class represents a collection of documents.
    The class provides methods to read the documents from a file,
    construct the inverted index, and calculate term frequencies.
"""


class Collection:
    def __init__(self, filename: str,
                 import_collection: bool = False,
                 export_collection: bool = False,
                 export_statistics: bool = False,
                 ltn_weighting: bool = False,
                 ltc_weighting: bool = False,
                 lnu_weighting: bool = False,
                 bm25_weighting: bool = False,
                 bm25fw_weighting: bool = False,
                 bm25fr_weighting: bool = False,
                 export_weighted_idx: bool = False,
                 parser_granularity: list = ['.//article'],
                 text_processor: TextProcessor = CustomTextProcessor()
                 ):

        if parser_granularity is None:
            parser_granularity = ['.//article']

        self.text_processor = text_processor
        self.filename = filename

        self.inverted_index = InvertedIndex(self.filename, self.text_processor, parser_granularity, is_bm25fr=bm25fr_weighting)
        self.label = filename.split('/')[-1].split('.')[0]

        # A dictionary with the term as key and a dictionary of document numbers and term frequencies as value
        # ex: {'term': {'doc1': 2, 'doc2': 1}}
        self.collection_frequencies = {}
        if (import_collection):
            granularity_str = '_'.join(parser_granularity).replace('.//', '')
            print(Fore.GREEN
                  + f'Importing collection : {self.label}_{granularity_str}' + Style.RESET_ALL)
            self.inverted_index.import_inverted_index(f'../res/{self.label}_{granularity_str}.json')
        else:
            print(Fore.GREEN + f'Indexing collection : {self.label}' + Style.RESET_ALL)
            self.inverted_index.construct_inverted_index()
            if export_collection:
                granularity_str = '_'.join(parser_granularity).replace('.//', '')
                self.inverted_index.export_inverted_index(f'../res/{self.label}_{granularity_str}.json')

        print(Fore.YELLOW + "> Indexing time:", self.inverted_index.indexing_time, "seconds" + Style.RESET_ALL)
        print()

        self.collection_size = len(self.inverted_index.parsed_documents)
        self.statistics = Statistics(self.inverted_index, export_statistics)

        if (ltn_weighting):
            self.print_title("LTN weighting")
            self.weighting_strategy = LTNWeighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        elif (ltc_weighting):
            self.print_title("LTC weighting")
            self.weighting_strategy = LTCWeighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        elif (lnu_weighting):
            self.print_title("LNU weighting")
            self.weighting_strategy = LNUWeighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        elif (bm25_weighting):
            self.print_title("BM25 weighting")
            self.weighting_strategy = BM25Weighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        elif (bm25fw_weighting):
            self.print_title("BM25Fw weighting")
            self.weighting_strategy = BM25FwWeighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        elif (bm25fr_weighting):
            self.print_title("BM25Fr weighting")
            self.weighting_strategy = BM25FrWeighting()
            self.weighted_index = self.weighting_strategy.calculate_weight(self)
        if (export_weighted_idx):
            WeightingStrategy().export_weighted_index(self.weighted_index, f'../res/{self.label}_weighted.json')

    def document_frequency(self, term: str, tag_cibled: str) -> int:
        """
        Returns the document frequency of a term.
        The document frequency is the sum of the frequencies of the term in all documents.
        # ! We compute the df based on the xpath and not on the entire document
        # - TO COMPUTE THE df based on the xpath use this formula:
        # - df = len(self.inverted_index.IDX.get(term, {}).get(xpath, {}))
        """
        docno_set = set()
        for x_path, docno_list in self.inverted_index.IDX.get(term, {}).items():
            tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
            if tag == tag_cibled:
                docno_set.update(docno_list)

        return len(docno_set)

    def term_frequency(self, docno: str, term: str, x_path: str) -> int:
        """
        Returns the term frequency of a term in a document at a specific XPath.
        """
        if term in self.inverted_index.TF and x_path in self.inverted_index.TF[term]:
            doc_freqs = self.inverted_index.TF[term][x_path]
            return doc_freqs.get(docno, 0)
        else:
            return 0

    def document_length(self, docno: str, granularity: str) -> int:
        """
        Returns the length of a document.
        The length of a document is the sum of the frequencies of all terms in the document
        based on the granularity.
        """
        return self.statistics.document_lengths[docno][granularity]

    def transform_index(self):
        """
        We transform the index to only contain the article node.
        """
        transformed_index = {}
        new_granularity = '/article[1]'

        transformed_index = {}
        for term, postings in self.inverted_index.IDX.items():
            transformed_index[term] = {}
            for _, docno_list in postings.items():
                if new_granularity not in transformed_index[term]:
                    transformed_index[term][new_granularity] = []

                for docno in docno_list:
                    if docno not in transformed_index[term][new_granularity]:
                        transformed_index[term][new_granularity].append(docno)

        self.inverted_index.IDX = transformed_index

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
