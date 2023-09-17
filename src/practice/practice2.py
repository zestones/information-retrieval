from exercise2.collections_manager import CollectionsManager
import sys


def main(_):
    collections_manager = CollectionsManager('../lib/data/test')
    
    # Index all documents in the folder
    collections_manager.calculate_collections_indexes()
    
    # collections_manager.display_collections_indexes()
    # collections_manager.calculate_collections_tf()
    # collections_manager.display_collections_tf()
    
    collections_manager.plot_indexing_time_by_collection_size()

if __name__ == "__main__":
    main(sys.argv[1:])
