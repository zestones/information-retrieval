from weighting_strategies.weighting_strategy import WeightingStrategy

import math
import time
import json


class BM25Weighting(WeightingStrategy):
    def __init__(self, k1=1, b=0.5):
        self.k1 = k1
        self.b = b

    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}
        start_time = time.time()

        N = collection.collection_size                       # Total number of documents in the collection
        avdl = collection.statistics.avg_collection_lengths  # Average document length in the collection

        for term, postings in collection.inverted_index.IDX.items():
            for granularity, entry in postings.items():
                df = collection.document_frequency(term, granularity)  # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))          # Inverse document frequency

                for docno, x_path in entry.items():
                    dl = collection.document_length(docno)          # Document length
                    tf = collection.term_frequency(docno, term, granularity)

                    # Calculate BM25 weight for the term in the document
                    weight = (tf * (self.k1 + 1)) / \
                        (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                    weight *= idf

                    # Update the weighted index
                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append(
                        {"XPath": x_path, "docno": docno, "weight": weight})

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index
