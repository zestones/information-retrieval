import statistics
import matplotlib.pyplot as plt


class Statistics:
    def __init__(self, collection):
        self.collection = collection

        self.document_lengths = []

        self.term_lengths_in_docs = []  # Number of terms in a document
        self.term_lengths_in_collection = []  # Number of terms in the collection

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

            term_length = len(set(tokens))
            self.term_lengths_in_docs.append(term_length)

            self.documents_vocabulary_sizes.append(len(set(tokens)))

        self.collection_vocabulary_sizes = len(set(self.collection.inverted_index.keys()))

        self.term_lengths_in_collection = sum(self.term_lengths_in_docs)
        self.collection.calculate_collection_frequencies()
        self.collection_frequency_of_terms = sum(
            list(self.collection.collection_frequencies.values()))
