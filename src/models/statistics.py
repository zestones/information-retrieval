import statistics
import json


class Statistics:
    def __init__(self, collection, export_statistics: bool = False) -> None:
        self.collection = collection

        self.documents_lengths = {}  # Length of each document in form of {docno: length}
        self.avg_collection_lengths = []  # Average document length in the collection

        self.avg_term_lengths_in_docs = []  # Average term length in each document
        self.avg_term_lengths_in_collection = []  # Average term length in the collection

        self.documents_vocabulary_sizes = []  # Number of unique terms in the each document
        self.collection_vocabulary_sizes = []  # Number of unique terms in the collection

        self.collection_frequency_of_terms = []  # Number of times a term appears in the collection

        # Resources folder to save the stats
        self.RESOURCES_FOLDER = '../docs/resources/'

        self.calculate_statistics()
        if (export_statistics):
            self.export_stats(f'stats-{self.collection.label}.json')

    def calculate_statistics(self):
        """
        Calculates statistics for the collection.
        """
        self.collection.calculate_collection_frequencies()

        for docno, data in self.collection.document_parser.parsed_documents.items():
            for entry in data:
                terms = entry["terms"]

                term_length = sum(len(term) for term in terms)
                self.avg_term_lengths_in_docs.append(
                    term_length / len(terms) if len(terms) > 0 else 0)

                self.documents_vocabulary_sizes.append(len(set(terms)))
                self.documents_lengths[docno] = len(terms)

        self.collection_vocabulary_sizes = len(set(self.collection.inverted_index.IDX.keys()))

        self.avg_collection_lengths = statistics.mean(
            self.documents_lengths.values()) if self.documents_lengths else 0
        self.avg_term_lengths_in_collection = statistics.mean(
            self.avg_term_lengths_in_docs) if self.avg_term_lengths_in_docs else 0

        self.collection_frequency_of_terms = sum(
            list(self.collection.collection_frequencies.values()))

    def export_stats(self, filename):
        """
        Exports all the statistics to a JSON file.
        """
        stats = {
            'indexing_time': self.collection.inverted_index.indexing_time,
            'avg_collection_lengths': self.avg_collection_lengths,
            'avg_term_lengths_in_collection': self.avg_term_lengths_in_collection,
            'collection_vocabulary_sizes': self.collection_vocabulary_sizes,
            'collection_frequency_of_terms': self.collection_frequency_of_terms,
        }

        with open(self.RESOURCES_FOLDER + filename, 'w') as outfile:
            json.dump(stats, outfile, indent=4)
