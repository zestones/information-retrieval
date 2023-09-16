from exercise2.text_processor import TextProcessor
from colorama import Fore, Style
import matplotlib.pyplot as plt
import os
import gzip 
import re
"""
    This class represents a collection of documents.
    The class provides methods to read the documents from a file, 
    construct the inverted index, and calculate term frequencies.
"""
class DocumentCollection:
    def __init__(self,file_name : str) -> None:
        self.text_processor = TextProcessor()
        self.inverted_index = {}
        self.collection_size = 0  
        self.document_lengths = [] 
        self.term_lengths = [] 
        self.vocabulary_sizes = [] 
        self.collection_frequencies = {} 
        self.file_name = file_name

    def read_document(self) -> list:
        """
        Reads the documents from the file.
        """
        if (self.file_name.endswith('.gz')):
            with gzip.open(self.file_name, 'rt', encoding='utf-8') as f:
                return self._read_document_lines(f.readlines())
        else:
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return self._read_document_lines(f.readlines())
        
    def _read_document_lines(self, lines: str) -> list:
        """
        Reads the documents from the content.
        """
        result = []
        current_content = ''
        current_docno = ''
        
        for line in lines:
            if '<doc><docno>' in line:
                docno = line.split('<doc><docno>')[1].split('</docno>')[0]
            elif '</doc>' in line: 
                result.append({ docno: current_content })
                current_content = ''
            else: current_content += line

        return result
    

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
    
    def calculate_collection_frequencies(self):
        """
        Calculate collection frequency of terms.
        """
        for term, postings in self.inverted_index.items():
            frequency = sum(self.term_frequency(docno, term) for docno in postings)
            self.collection_frequencies[term] = frequency

    def construct_inverted_index(self, collection: list) -> dict:
        """
        Constructs the inverted index and computes statistics.
        """
        index = {}
        term_frequencies = {}
        for doc in collection:
            docno = list(doc.keys())[0]
            content = list(doc.values())[0]

            tokens = self.text_processor.post_processing(content)

            doc_length = len(tokens)  # Calculate document length
            self.document_lengths.append(doc_length)

            for token in tokens:
                if token not in index:
                    index[token] = [docno]
                    term_frequencies[token] = {docno: 1}
                else:
                    term_frequencies.setdefault(token, {}).setdefault(docno, 0)
                    term_frequencies[token][docno] += 1

                    if docno not in index[token]:
                        index[token].append(docno)

            # Calculate term length and update vocabulary size
            term_length = len(index) 
            self.term_lengths.append(term_length)
            self.vocabulary_sizes.append(len(index)) # TODO: not sure if we should count unique terms

        self.inverted_index = index
        self.term_frequencies = term_frequencies
        # TODO: not sure if this is the best way to calculate collection size 
        self.collection_size = len(collection)

    def print_title(self, text: str) -> None:
        """
        Prints a title.
        """
        print(Fore.BLUE + text + Style.RESET_ALL)
        print('-' * len(text))

    def plot_statistics(self):
        """
        Plot the evolution of statistics as the collection size grows.
        """
        plt.figure(figsize=(12, 6))

        plt.subplot(2, 2, 1)
        plt.plot(range(self.collection_size), self.document_lengths)
        plt.xlabel('Collection Size')
        plt.ylabel('Document Length')
        plt.title('Document Length Evolution')

        plt.subplot(2, 2, 2)
        plt.plot(range(self.collection_size), self.term_lengths)
        plt.xlabel('Collection Size')
        plt.ylabel('Term Length')
        plt.title('Term Length Evolution')

        plt.subplot(2, 2, 3)
        plt.plot(range(self.collection_size), self.vocabulary_sizes)
        plt.xlabel('Collection Size')
        plt.ylabel('Vocabulary Size')
        plt.title('Vocabulary Size Evolution')

        plt.subplot(2, 2, 4)
        terms = list(self.collection_frequencies.keys())
        frequencies = list(self.collection_frequencies.values())
        plt.barh(terms, frequencies)
        plt.xlabel('Collection Frequency')
        plt.ylabel('Terms')
        plt.title('Collection Frequency of Terms')

        plt.tight_layout()
        plt.show()

    def display_inverted_index(self):
        """
        Displays the inverted index with a title indicating the document name.
        """
        self.print_title(f"\nInverted Index of '{self.file_name}\n'")
        for term, docnos in self.inverted_index.items():
            docno_list = ', '.join([f'{Fore.GREEN}{docno}{Style.RESET_ALL}' for docno in docnos])
            print(f"{term}: {docno_list}")
        print()

    def display_term_frequencies(self) -> None:
        """
        Displays the term frequencies.
        """
        self.print_title('Term Frequencies')
        
        for term in self.term_frequencies:
            print(term, end=': ')
            for docno in self.term_frequencies[term]:
                print(Fore.GREEN + docno + Style.RESET_ALL + '(' + str(self.term_frequencies[term][docno]) + ')', end=' ')
            print()
        
        print()