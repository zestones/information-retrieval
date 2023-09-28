from manager.collections_manager import CollectionsManager
import sys


def main(_):
    collections_manager = CollectionsManager('../lib/data/test')
    collections_manager.plot_statistics()


if __name__ == "__main__":
    main(sys.argv[1:])
