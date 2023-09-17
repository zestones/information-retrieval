import os
from exercise2.document_collection import DocumentCollection
import time
import matplotlib.pyplot as plt


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
                end_time = time.time()
            
                self.collections.append(collection)
                
                indexing_time = end_time - start_time
                indexing_times.append(indexing_time)
            
        self.collection_sizes = [collection.collection_size for collection in self.collections]
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
            
    def plot_statistics(self):
        """
        Display statistics for all collections.
        """
        # Sub plots (bar chart) of document lengths by collection size
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        
        # sum of document lengths array
        for collection in self.collections:
            document_lengths = [sum(collection.document_lengths) for collection in self.collections]
            plt.bar(range(len(document_lengths)), document_lengths)
            
        plt.xlabel('Collection Size')
        plt.ylabel('Document Length')
        plt.title('Document Length Evolution')

        # Sub plots (bar chart) of term lengths by collection size
        plt.subplot(2, 2, 2)
        for collection in self.collections:
            term_lengths = [len(collection.term_lengths) for collection in self.collections]
            plt.bar(range(len(term_lengths)), term_lengths)
            
        plt.xlabel('Collection Size')
        plt.ylabel('Term Length')
        plt.title('Term Length Evolution')
       
        # Sub plots of collection frequencies by collection size
        plt.subplot(2, 2, 4)
        for collection in self.collections:
            terms = list(collection.collection_frequencies.keys())
            frequencies = list(collection.collection_frequencies.values())
            plt.barh(terms, frequencies)
            
        plt.xlabel('Collection Frequency')
        plt.ylabel('Terms')
        plt.title('Collection Frequency of Terms')
        
        plt.tight_layout()
        plt.show()
        
    def plot_efficiency(self, size_values, time_values):
        plt.figure(figsize=(10, 6))
        plt.plot(size_values, time_values, marker='o', linestyle='-')
        plt.title('Efficiency vs. Collection Size')
        plt.xlabel('Collection Size')
        plt.ylabel('Time (seconds)')
        plt.grid(True)
        plt.show()