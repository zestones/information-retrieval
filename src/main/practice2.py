from manager.collections_manager import CollectionsManager
import sys


def main(_):
    collections_manager = CollectionsManager('../lib/data/practice_02')

    # collections_manager.display_collections_indexes()
    # collections_manager.calculate_collections_tf()
    # collections_manager.display_collections_tf()

    collections_manager.plot_indexing_time_by_collection_size()
    collections_manager.plot_statistics()


if __name__ == "__main__":
    main(sys.argv[1:])
