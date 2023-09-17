from exercise2.collection import Collection
import matplotlib.pyplot as plt
import time
import os


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
            
        self.collection_sizes = [collection.collection_size for collection in self.collections]

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
        collection_size_label = 'Collection Size'
        
        # Sub plots (bar chart) of document lengths by collection size
        plt.figure(figsize=(10, 6))
        plt.subplot(2, 2, 1)
        
        # sum of document lengths array
        for collection in self.collections:
            document_lengths = [sum(collection.document_lengths) for collection in self.collections]
            plt.bar(range(len(document_lengths)), document_lengths)
            
        plt.xlabel(collection_size_label)
        plt.ylabel('Document Length')
        plt.title('Document Length Evolution')

        # Sub plots (bar chart) of term lengths by collection size
        plt.subplot(2, 2, 2)
        for collection in self.collections:
            term_lengths = [len(collection.term_lengths) for collection in self.collections]
            plt.bar(range(len(term_lengths)), term_lengths)
            
        plt.xlabel(collection_size_label)
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
        
        plt.savefig(self.RESOURCES_FOLDER + 'statistics.png')
        plt.show()
        
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