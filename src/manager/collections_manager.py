import numpy as np
import os
import time
from models.collection import Collection
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


"""
This class represents a collection of collections.
The class provides methods to read the documents from a file,
construct the inverted index, and calculate term frequencies.
"""


class CollectionsManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path

        self.collections = []

        # Stats
        self.indexing_times = []

        # Resources folder to save the plots
        self.RESOURCES_FOLDER = '../docs/practice_02/resources/'

        # Index all collections in the folder
        self.calculate_collections_indexes()

    def calculate_collections_indexes(self):
        """
        Indexes all documents in the folder.
        """
        # List all files in the folder
        filenames = os.listdir(self.folder_path)

        for filename in filenames:
            if filename.endswith('.gz'):
                file_path = os.path.join(self.folder_path, filename)

                # Create a Collection for each file

                start_time = time.time()
                collection = Collection(file_path)
                end_time = time.time()

                self.collections.append(collection)

                indexing_time = end_time - start_time
                self.indexing_times.append(indexing_time)

    def calculate_collections_tf(self):
        """
        Calculate collection frequencies for all collections.
        """
        for collection in self.collections:
            collection.calculate_collection_frequencies()

    def display_collections_tf(self):
        """
        Displays term frequencies for all collections.
        """
        for collection in self.collections:
            collection.display_term_frequencies()

    def display_collections_indexes(self):
        """
        Display inverted_index for all collections.
        """
        for collection in self.collections:
            collection.display_inverted_index()

    def plot_statistics(self):
        """
        Display statistics for all collections.
        """
        self.plot_indexing_time_by_collection_size()
        self.plot_document_length_evolution()
        self.plot_term_length_evolution()
        self.plot_vocabulary_size_evolution()
        self.plot_collection_frequency_of_terms_evolution()

    def plot_indexing_time_by_collection_size(self):
        """
        Display efficiency for all collections.
        """
        plt.figure(figsize=(10, 6))

        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections]
        plt.plot(collection_sizes, self.indexing_times, marker='o', linestyle='-')

        plt.title('Indexing Time by Collection Size')
        plt.xlabel('Collection Size')
        plt.ylabel('Time (seconds)')
        plt.grid(True)

        plt.savefig(self.RESOURCES_FOLDER + 'indexing_time_by_collection_size.png')
        plt.show()

    # STATISTICS
    # TODO: move to stats class

    def plot_document_length_evolution(self):
        """
        Plot the evolution of document length as the collection size grows.
        """
        plt.figure(figsize=(10, 6))

        for collection in self.collections:
            collection_sizes = [
                collection.collection_statistics.collection_size] * len(collection.collection_statistics.document_lengths)

            document_lengths = collection.collection_statistics.document_lengths

            plt.plot(collection_sizes, document_lengths, marker='o',
                     linestyle='-', label=collection.label)

        plt.title('Document Length Evolution')
        plt.xlabel('Collection Size')
        plt.ylabel('Document Length')
        plt.grid(True)
        plt.legend()

        plt.savefig(self.RESOURCES_FOLDER + 'document_length_evolution.png')
        plt.show()

    def plot_term_length_evolution(self):
        """
        Plot the evolution of term length as the collection size grows.
        TODO : fix this plot (hard to read)
        """

        # Extract collection sizes and term lengths
        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections]
        term_lengths = [
            collection.collection_statistics.term_lengths_in_collection for collection in self.collections]

        plt.figure(figsize=(20, 6))
        for i in range(len(self.collections)):
            plt.bar(
                collection_sizes[i],
                term_lengths[i],
                label=self.collections[i].label,
                alpha=0.5
            )

        plt.title('Term Length Evolution')
        plt.xlabel('Collection Size')
        plt.ylabel('Term Length')
        plt.legend()

        plt.savefig(self.RESOURCES_FOLDER + 'term_length_evolution.png')
        plt.show()

    def plot_vocabulary_size_evolution(self):
        """
        Plot the evolution of vocabulary size as the collection size grows.
        """
        plt.figure(figsize=(10, 6))

        for collection in self.collections:
            collection_sizes = [
                collection.collection_statistics.collection_size] * len(collection.collection_statistics.documents_vocabulary_sizes)

            vocabulary_sizes = collection.collection_statistics.documents_vocabulary_sizes

            plt.plot(collection_sizes, vocabulary_sizes, marker='o',
                     linestyle='-', label=collection.label)

        plt.title('Vocabulary Size Evolution')
        plt.xlabel('Collection Size')
        plt.ylabel('Vocabulary Size')
        plt.grid(True)
        plt.legend()

        plt.savefig(self.RESOURCES_FOLDER + 'vocabulary_size_evolution.png')
        plt.show()

    def plot_collection_frequency_of_terms_evolution(self):
        """
        Plot the evolution of collection frequency of terms as the collection size grows.
        TODO : fix this plot (hard to read and possibly wrong)
        """
        plt.figure(figsize=(10, 6))

        # Extract collection sizes and term lengths
        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections]
        collection_frequencies = [
            collection.collection_statistics.collection_frequency_of_terms for collection in self.collections]

        plt.figure(figsize=(20, 6))
        for i in range(len(self.collections)):
            plt.bar(
                collection_sizes[i],
                collection_frequencies[i],
                label=self.collections[i].label,
                alpha=0.5
            )

        plt.title('Collection Frequency of Terms Evolution')
        plt.xlabel('Collection Size')
        plt.ylabel('Collection Frequency of Terms')
        plt.legend()

        plt.savefig(self.RESOURCES_FOLDER + 'collection_frequency_of_terms_evolution.png')
        plt.show()
