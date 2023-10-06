from manager.collections_manager import CollectionsManager

from colorama import Fore, Style
import getopt
import sys


def print_usage():
    print(Fore.YELLOW + Style.BRIGHT + "Usage:" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Options:" + Style.RESET_ALL)
    print(Fore.CYAN + "-h, --help".ljust(40)
          + Style.RESET_ALL + "Display this help message")
    print(Fore.CYAN + "-d, --display".ljust(40)
          + Style.RESET_ALL + "Display inverted indexes")
    print(Fore.CYAN + "-p, --plot".ljust(40)
          + Style.RESET_ALL + "Plot statistics")
    print(Fore.CYAN + "-i, --indexing-time".ljust(40)
          + Style.RESET_ALL + "Plot indexing time by collection size")
    sys.exit(2)


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "hdpi", ["help", "display", "plot", "indexing-time"])
    except getopt.GetoptError:
        print_usage()

    display_collections = False
    plot_statistics = False
    plot_indexing_time = False

    for opt, _ in opts:
        if opt in ("-d", "--display"):
            display_collections = True
        elif opt in ("-p", "--plot"):
            plot_statistics = True
        elif opt in ("-i", "--indexing-time"):
            plot_indexing_time = True
        elif opt in ("-h", "--help"):
            print_usage()

    collections_manager = CollectionsManager('../lib/data/practice_02/', statistics=plot_statistics)

    if display_collections:
        collections_manager.display_collections_indexes()

    if plot_statistics:
        collections_manager.plot_statistics()

    if plot_indexing_time:
        collections_manager.plot_indexing_time_by_collection_size()


if __name__ == "__main__":
    main(sys.argv[1:])
