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
        self.collection_sizes = []

        # Stats
        self.indexing_times = []

        # Resources folder to save the plots
        self.RESOURCES_FOLDER = '../docs/practice-2/resources/'

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
                collection = Collection(file_path)

                start_time = time.time()
                collection.construct_inverted_index()
                end_time = time.time()

                self.collections.append(collection)

                indexing_time = end_time - start_time
                self.indexing_times.append(indexing_time)

        self.collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections]

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
        for collection in self.collections:
            collection.collection_statistics.plot_statistics()

    def plot_indexing_time_by_collection_size(self):
        """
        Display efficiency for all collections.
        """
        plt.figure(figsize=(10, 6))
        plt.plot(self.collection_sizes, self.indexing_times, marker='o', linestyle='-')

        plt.title('Indexing Time by Collection Size')
        plt.xlabel('Collection Size')
        plt.ylabel('Time (seconds)')
        plt.grid(True)

        plt.savefig(self.RESOURCES_FOLDER + 'efficiency.png')
        plt.show()
