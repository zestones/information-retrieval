from exercise2.document_collection import DocumentCollection

from colorama import Fore, Style
import getopt
import sys


def main(argv):
    document_collection = DocumentCollection()
    collection = document_collection.read_documents('../lib/data/practice_02')
    document_collection.construct_inverted_index(collection)

    # Calculate the collection frequencies
    document_collection.calculate_collection_frequencies()

    # Plot the evolution of statistics
    document_collection.plot_statistics()


if __name__ == "__main__":
    main(sys.argv[1:])
