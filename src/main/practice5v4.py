from manager.run_manager.run_manager import RunManager

import argparse
import sys

import argparse


def main(argv):
    parser = argparse.ArgumentParser(description='Process command-line options.')
    parser.add_argument('-d', '--display', action='store_true', help='Display collections indexes')
    parser.add_argument('-p', '--plot', action='store_true', help='Plot statistics')
    
    parser.add_argument('-t', '--indexing-time', action='store_true', help='Plot indexing time by collection size')
    parser.add_argument('-e', '--export-inverted-index', action='store_true', help='Export collection')
    parser.add_argument('-i', '--import-inverted-index', action='store_true', help='Import collection')
    
    parser.add_argument('-s', '--statistics', action='store_true', help='Export statistics')
    parser.add_argument('--ltn', action='store_true', help='Use LTN weighting')
    parser.add_argument('--ltc', action='store_true', help='Use LTC weighting, length normalization and cosine similarity')
    
    parser.add_argument('--bm25', action='store_true', help='Use BM25 weighting scheme')
    parser.add_argument('--bm25fw', action='store_true', help='Use BM25Fw weighting scheme')
    parser.add_argument('--bm25fr', action='store_true', help='Use BM25Fr weighting scheme')
    
    parser.add_argument('--cos-sim', action='store_true', help='Use cosine similarity for evaluation')
    parser.add_argument('--export-weighted-idx', action='store_true', help='Export weighted index to JSON file')
    parser.add_argument('--query-file', type=str, help='File containing queries')
    
    parser.add_argument('-g', '--granularity', type=str, nargs='+', help='Granularity of the XPath query')
    parser.add_argument('--baseline', action='store_true', help='Run baseline')
    parser.add_argument('-o', '--bm25_optimization', action='store_true', help='Run BM25 parameter optimization experiment')
    
    args = parser.parse_args(argv)

    RunManager(args).run()


if __name__ == "__main__":
    main(sys.argv[1:])
