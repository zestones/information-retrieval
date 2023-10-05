import statistics
import matplotlib.pyplot as plt


import csv

class Statistics:
    def __init__(self, collection):
        self.collection = collection

        self.document_lengths = []

        self.avg_term_lengths_in_docs = []  # Average term length in each document
        self.avg_term_lengths_in_collection = []  # Average term length in the collection

        self.documents_vocabulary_sizes = []  # Number of unique terms in the each document
        self.collection_vocabulary_sizes = []  # Number of unique terms in the collection

        self.collection_frequency_of_terms = []  # Number of times a term appears in the collection

        # Resources folder to save the plots
        self.RESOURCES_FOLDER = '../docs/practice_02/resources/'
        self.calculate_statistics()

    def calculate_statistics(self):
        """
        Calculates statistics for the collection.
        """

        for doc in self.collection.parsed_documents:
            content = list(doc.values())[0]
            tokens = self.collection.text_processor.pre_processing(content)

            self.document_lengths.append(len(tokens))

            term_length = sum(len(token) for token in tokens)
            self.avg_term_lengths_in_docs.append(term_length / len(tokens))

            self.documents_vocabulary_sizes.append(len(set(tokens)))

        self.collection_vocabulary_sizes = len(set(self.collection.inverted_index.keys()))

        self.avg_term_lengths_in_collection = statistics.mean(self.avg_term_lengths_in_docs)
        self.collection.calculate_collection_frequencies()
        self.collection_frequency_of_terms = sum(
            list(self.collection.collection_frequencies.values()))

    def export_stats(self, filename):
        """
        Exports all the statistics to a CSV file.
        """
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Statistic', 'Value'])
            writer.writerow(['Number of documents', len(self.collection.parsed_documents)])
            writer.writerow(['Average document length', statistics.mean(self.document_lengths)])
            writer.writerow(['Average term length in collection', self.avg_term_lengths_in_collection])
            writer.writerow(['Number of unique terms in collection', self.collection_vocabulary_sizes])
            writer.writerow(['Total number of terms in collection', self.collection_frequency_of_terms])
            writer.writerow(['Document vocabulary sizes'])
            for i, size in enumerate(self.documents_vocabulary_sizes):
                writer.writerow([f'Document {i+1}', size])
