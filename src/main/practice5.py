from models.collection import Collection
from manager.query_manager import QueryManager
from manager.text_processor import CustomTextProcessor
from manager.text_processor import NltkTextProcessor

from weighting_strategies.bm25_weighting import BM25Weighting

from colorama import Fore, Style
import argparse
import sys

import argparse
import os
import numpy as np


def parse_query_file(query_file):
    parsed_queries = []
    with open(query_file, 'r') as file:
        for line in file:
            if not line.strip():
                continue
            parts = line.strip().split(' ', 1)

            if len(parts) == 2:
                query_id, query = parts
                parsed_queries.append((query_id, query))

    print(parsed_queries)
    return parsed_queries


def launch_query(query_id, query, run_id, collection):
    query_manager = QueryManager(collection)

    res = query_manager.RSV(query)
    query_results = query_manager.format_query_results(query_id, res, run_id)

    return query_results


def construct_run_name(run_id, weighting_scheme, k1=None, b=None):
    return "../docs/resources/runs/BengezzouIdrissMezianeGhilas_" + str(run_id) + "_" + weighting_scheme + "_articles_stop671_porter_k" + str(k1) + "_b" + str(b) + ".txt"


def write_results(query_results, run_file_path):
    with open(run_file_path, 'a') as output_file:
        for result in query_results:
            output_file.write(
                f"{result[0]} {result[1]} {result[2]} {result[3]} {result[4]} {result[5]} {result[6]}\n")


def get_run_id(folder_path):
    # Compute the number of files in the folder
    # The run id is the number of files + 1
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    return len(files) + 1


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

    collection = Collection('../lib/data/practice_05/Practice_05_data.zip',
                            plot_statistics=args.plot,
                            import_collection=args.import_inverted_index,
                            export_collection=args.export_inverted_index,
                            export_statistics=args.statistics,
                            ltn_weighting=args.ltn,
                            ltc_weighting=args.ltc,
                            bm25_weighting=args.bm25,
                            export_weighted_idx=args.export_weighted_idx
                            )

    query_manager = QueryManager(collection)

    while True:
        query = input("Enter a query (q to quit):\n> ").strip(" ")

        if query.lower() == 'q' or query.lower() == 'quit':
            break

        res = query_manager.RSV(query)
        query_manager.print_query_results(query, res)


if __name__ == "__main__":
    main(sys.argv[1:])
