import os
import time
from models.collection import Collection
from manager.plots_manager import PlotsManager

"""
This class represents a collection of collections.
The class provides methods to read the documents from a file,
construct the inverted index, and calculate term frequencies.
"""


class CollectionsManager:
    def __init__(self, folder_path, statistics=False, import_collection=False, export_collection=False):
        self.folder_path = folder_path

        self.collections = []

        # Stats
        self.indexing_times = []
        self.statistics = statistics

        # Collection parameters
        self.import_collection = import_collection
        self.export_collection = export_collection

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

                collection = Collection(file_path, statistics=self.statistics,
                                        import_collection=self.import_collection, export_collection=self.export_collection)
                self.collections.append(collection)
                self.indexing_times.append(collection.indexing_time)

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
        plots_manager = PlotsManager(self)
        plots_manager.plot_document_length_evolution()
        plots_manager.plot_term_length_evolution()
        plots_manager.plot_vocabulary_size_evolution()
        plots_manager.plot_collection_frequency_of_terms_evolution()

    def plot_indexing_time_by_collection_size(self):
        """
        Display efficiency for all collections.
        """
        plots_manager = PlotsManager(self)
        plots_manager.plot_indexing_time_by_collection_size()
