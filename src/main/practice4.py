from models.collection import Collection
from manager.query_manager import QueryManager


from colorama import Fore, Style
import argparse
import sys


import argparse

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
    parser.add_argument('--bm25', action='store_true', help='Use BM25 weighting scheme')
    parser.add_argument('--cos-sim', action='store_true',
                        help='Use cosine similarity for evaluation')
    parser.add_argument('--export-weighted-idx', action='store_true',
                        help='Export weighted index to JSON file')
    parser.add_argument('--query-file', type=str, help='File containing queries')

    args = parser.parse_args(argv)

    collection = Collection('../lib/data/practice_03/Practice_03_data.zip',
                            plot_statistics=args.plot,
                            import_collection=args.import_inverted_index,
                            export_collection=args.export_inverted_index,
                            export_statistics=args.statistics,
                            ltn_weighting=args.ltn,
                            ltc_weighting=args.ltc,
                            bm25_weighting=args.bm25,
                            export_weighted_idx=args.export_weighted_idx
                            )

    if args.query_file:
        query_manager = QueryManager(collection)
        with open(args.query_file, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    query_id, query = parts
                    print(query_id+"query:"+query)
                    if args.cos_sim:
                        res = query_manager.cosine_similarity(query)
                    else:
                        res = query_manager.RSV(query)

                    query_manager.print_query_results(query_id, res) 


if __name__ == "__main__":
    main(sys.argv[1:])

