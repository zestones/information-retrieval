from models.collection import Collection
from manager.query_manager import QueryManager


from colorama import Fore, Style
import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description='Process command-line options.')
    parser.add_argument('-d', '--display', action='store_true', help='Display collections indexes')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot statistics')
    parser.add_argument('-t', '--indexing-time', action='store_true',
                        help='Plot indexing time by collection size')
    parser.add_argument('-e', '--export-inverted-index',
                        action='store_true', help='Export collection')
    parser.add_argument('-i', '--import-inverted-index',
                        action='store_true', help='Import collection')
    parser.add_argument('-s', '--statistics', action='store_true', help='Export statistics')
    parser.add_argument('--ltn', action='store_true', help='Use LTN weighting')
    parser.add_argument('--ltc', action='store_true',
                        help='Use LTC weighting, length normalization and cosine similarity')

    args = parser.parse_args(argv)

    collection = Collection('../lib/data/practice_03/Practice_03_data.zip',
                            plot_statistics=args.plot,
                            import_collection=args.import_inverted_index,
                            export_collection=args.export_inverted_index,
                            export_statistics=args.statistics,
                            ltn_weighting=args.ltn,
                            ltc_weighting=args.ltc)

    if args.display:
        collection.display_collections_indexes()

    if args.plot:
        collection.plot_all_statistics()

    if args.indexing_time:
        collection.plot_indexing_time_by_collection_size()

    if args.ltn:
        query_manager = QueryManager(collection)
        while True:
            query = input("Enter a query" + Fore.YELLOW
                          + " (q to quit):\n> " + Style.RESET_ALL).strip(" ")

            if query.lower() == 'q' or query.lower() == 'quit':
                break

            res = query_manager.evaluate_query(query)
            query_manager.print_query_results(query, res)

    elif args.ltc:
        query_manager = QueryManager(collection)
        while True:
            query = input("Enter a query" + Fore.YELLOW
                          + " (q to quit):\n> " + Style.RESET_ALL).strip(" ")

            if query.lower() == 'q' or query.lower() == 'quit':
                break

            res = query_manager.evaluate_ltc_query(query)
            query_manager.print_query_results(query, res)


if __name__ == "__main__":
    main(sys.argv[1:])
