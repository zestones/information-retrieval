import statistics
import json

import time


class Statistics:
    def __init__(self, collection, export_statistics: bool = False, plot_statistics: bool = False) -> None:
        self.collection = collection

        self.avg_document_lengths = []
        self.avg_collection_lengths = []

        self.avg_term_lengths_in_docs = []  # Average term length in each document
        self.avg_term_lengths_in_collection = []  # Average term length in the collection

        self.documents_vocabulary_sizes = []  # Number of unique terms in the each document
        self.collection_vocabulary_sizes = []  # Number of unique terms in the collection

        self.collection_frequency_of_terms = []  # Number of times a term appears in the collection

        # Resources folder to save the stats
        self.RESOURCES_FOLDER = '../docs/resources/'

        if (plot_statistics or export_statistics):
            start_time = time.time()
            self.calculate_statistics()
            end_time = time.time()
            print(f'Calculated statistics in {end_time - start_time} seconds')
        if (export_statistics):
            self.export_stats(f'stats-{self.collection.label}.json')

    def calculate_statistics(self):
        """
        Calculates statistics for the collection.
        """
        self.collection.calculate_collection_frequencies()

        for doc in self.collection.parsed_documents:
            tokens = list(doc.values())[0]

            term_length = sum(len(token) for token in tokens)
            self.avg_term_lengths_in_docs.append(term_length / len(tokens))

            self.documents_vocabulary_sizes.append(len(set(tokens)))
            self.avg_document_lengths.append(len(tokens))

        self.collection_vocabulary_sizes = len(set(self.collection.inverted_index.keys()))

        self.avg_collection_lengths = statistics.mean(self.avg_document_lengths)
        self.avg_term_lengths_in_collection = statistics.mean(self.avg_term_lengths_in_docs)

        self.collection_frequency_of_terms = sum(
            list(self.collection.collection_frequencies.values()))

    def export_stats(self, filename):
        """
        Exports all the statistics to a JSON file.
        """
        stats = {
            'indexing_time': self.collection.indexing_time,
            'avg_collection_lengths': self.avg_collection_lengths,
            'avg_term_lengths_in_collection': self.avg_term_lengths_in_collection,
            'collection_vocabulary_sizes': self.collection_vocabulary_sizes,
            'collection_frequency_of_terms': self.collection_frequency_of_terms,
        }

        with open(self.RESOURCES_FOLDER + filename, 'w') as outfile:
            json.dump(stats, outfile, indent=4)
