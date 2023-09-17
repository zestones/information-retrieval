from exercise2.boolean_query_parser import BooleanQueryParser
from exercise2.collection import Collection

from colorama import Fore, Style
import getopt
import sys

SIMPLE_EXAMPLE_FILE = '../lib/data/practice_01/example_queries/simple_queries.txt'
COMPLEX_EXAMPLE_FILE = '../lib/data/practice_01/example_queries/complex_queries.txt'


def print_usage():
    print(Fore.YELLOW + Style.BRIGHT + "Usage:" + Style.RESET_ALL)
    print(Fore.CYAN + Style.BRIGHT + "Options:" + Style.RESET_ALL)
    print(Fore.CYAN + "-h, --help".ljust(40) + Style.RESET_ALL + "Display this help message")
    print(Fore.CYAN + "-e, --example".ljust(40) + Style.RESET_ALL + "Run example queries")
    print(Fore.CYAN + "-i, --interactive".ljust(40) + Style.RESET_ALL + "Enter interactive mode")
    print(Fore.CYAN + "--inverted_index".ljust(40) + Style.RESET_ALL + "Display the index")
    print(Fore.CYAN + "--term_frequencies".ljust(40) + Style.RESET_ALL + "Display term frequencies")

def print_query(queries: list, query_parser: BooleanQueryParser):
    for query in queries:
        result = query_parser.evaluate_query(query)
        print(Style.BRIGHT + "Query: " + Style.RESET_ALL + query)
        print(Fore.GREEN + "Result: " + Style.RESET_ALL + ', '.join(result))
        print()

def read_query_file(filename: str):
    with open(filename, 'r') as f: queries = f.readlines()
    queries = [query.strip() for query in queries]
    return queries


def run_example(collection: Collection):
    query_parser = BooleanQueryParser(collection.inverted_index)

    collection.print_title("Simple queries")
    simple_queries = read_query_file(SIMPLE_EXAMPLE_FILE)
    print_query(simple_queries, query_parser)

    collection.print_title("Complex queries")
    complex_queries = read_query_file(COMPLEX_EXAMPLE_FILE)
    print_query(complex_queries, query_parser)


def run_interactive_mode(collection: Collection):
    query_parser = BooleanQueryParser(collection.inverted_index)

    while True:
        query = input("Enter a query" + Fore.YELLOW + " (q to quit):\n> " + Style.RESET_ALL).strip(" ")
        if query.lower() == 'q' or query.lower() == 'quit': break

        if not query:
            print(Fore.RED + "Invalid query" + Style.RESET_ALL)
            continue

        result = query_parser.evaluate_query(query)
        if (len(result) == 0): print(Fore.RED + "No results found" + Style.RESET_ALL)
        else: print(Fore.GREEN + "Result: " + Style.RESET_ALL + ', '.join(result))
        print()


def main(argv):
    try:
        opts, _ = getopt.getopt(argv, "heip", ["help", "example", "interactive", "inverted_index", "term_frequencies"])
    except getopt.GetoptError:
        print("Invalid option. Use -h or --help for usage information.")
        sys.exit(-1)

    collection = Collection('../lib/data/practice_01/collection.xml')

    for opt, _ in opts:
        if opt in ("-h", "--help"): print_usage()
        elif opt in ("-e", "--example"): run_example(collection)
        elif opt in ("-i", "--interactive"): run_interactive_mode(collection)
        elif opt == "--inverted_index": collection.display_inverted_index()
        elif opt == "--term_frequencies": collection.display_term_frequencies()

if __name__ == "__main__":
    main(sys.argv[1:])
