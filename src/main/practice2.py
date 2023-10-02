from manager.collections_manager import CollectionsManager
import getopt
import sys
from colorama import Fore,Style

def print_usage():
    print(Fore.YELLOW + Style.BRIGHT + "Usage:" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Options:" + Style.RESET_ALL)
    print(Fore.CYAN + "-h, --help".ljust(40)
          + Style.RESET_ALL + "Display this help message")
    print(Fore.CYAN + "-d, --display".ljust(40)
          + Style.RESET_ALL + "Display inverted indexes")
    print(Fore.CYAN + "-p, --plot".ljust(40)
          + Style.RESET_ALL + "Plot statistics")
    sys.exit(2)
    
    
def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "hdp", ["help", "display", "plot"])
    except getopt.GetoptError:
        print_usage()
        
    display_collections = False
    plot_statistics = False

    for opt, _ in opts:
        if opt in ("-d", "--display"):
            display_collections = True
        elif opt in ("-p", "--plot"):
            plot_statistics = True
        elif opt in ("-h", "--help"):
            print_usage()


    collections_manager = CollectionsManager('../lib/data/test/')

    if display_collections:
        collections_manager.display_collections_indexes()

    if plot_statistics:
        collections_manager.plot_statistics()

if __name__ == "__main__":
    main(sys.argv[1:])
