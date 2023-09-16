from exercise2.document_collection import DocumentCollection
from exercise2.collections_manager import CollectionsManager
from colorama import Fore, Style
import getopt
import sys


def main(argv):
    collections_manager = CollectionsManager('../lib/data/test')
    # Index all documents in the folder
    indexing_times = collections_manager.calculate_collections_indexes()
    collections_manager.display_collections_indexes()
    collections_manager.calculate_collections_tf()
    collections_manager.display_collections_tf()
    collection_sizes = [10, 20, 50]
    collections_manager.plot_efficiency(collection_sizes, indexing_times)

if __name__ == "__main__":
    main(sys.argv[1:])
