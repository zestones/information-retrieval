import os
from exercise2.document_collection import DocumentCollection
import time
import matplotlib.pyplot as plt

class CollectionsManager:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.collections = []

    def calculate_collections_indexes(self):
        """
        Indexes all documents in the folder.
        """
        # List all files in the folder
        file_names = os.listdir(self.folder_path)
        indexing_times = []

        for file_name in file_names:
            if file_name.endswith('.gz'):
                # Construct the full path to the compressed document
                full_path = os.path.join(self.folder_path, file_name)
                # Create a DocumentCollection for each file
                collection = DocumentCollection(full_path)
                file_collection = collection.read_document()
                start_time = time.time()
                collection.construct_inverted_index(file_collection)
                self.collections.append(collection)
                end_time = time.time()
            indexing_time = end_time - start_time
            indexing_times.append(indexing_time)
        return indexing_times

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

    def plot_efficiency(self, size_values, time_values):
        plt.figure(figsize=(10, 6))
        plt.plot(size_values, time_values, marker='o', linestyle='-')
        plt.title('Efficiency vs. Collection Size')
        plt.xlabel('Collection Size')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.show()