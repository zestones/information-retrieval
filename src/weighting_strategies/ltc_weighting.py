from weighting_strategies.weighting_strategy import WeightingStrategy
from weighting_strategies.ltn_weighting import LTNWeighting

import math
import time

import numpy as np


class LTCWeighting(WeightingStrategy):
    def calculate_weight(self, collection):
        """
        Constructs the weighted index using the LTC weighting scheme.
        """
        weighted_index = LTNWeighting().calculate_weight(collection)
        return self.length_normalization(collection, weighted_index)

    def length_normalization(self, collection, weighted_index):
        """
        Normalizes the weights in the weighted index using the length normalization formula.
        """
        start_time = time.time()

        sum_of_squares_dict = self._compute_sum_of_squares(collection, weighted_index)

        # Normalize the weights
        for term, postings in collection.inverted_index.IDX.items():
            for docno in postings:
                sum_of_squares = sum_of_squares_dict[docno]

                # Calculate the normalization factor
                # w(i, d): Weight of term 'term' in document 'docno' before normalization
                normalization_factor = 1.0 / math.sqrt(sum_of_squares)

                # Apply the length normalization to the weight for term 'term' in document 'docno'
                # w_ln(i, d): Weight of term 'term' in document 'docno' after length normalization
                weighted_index[term][docno] *= normalization_factor

        end_time = time.time()
        self.print_normalization_time(start_time, end_time)
        return weighted_index

    def _compute_sum_of_squares(self, collection, weighted_index):
        """
        Computes the sum of squares for each document in the collection.
        """
        sum_of_squares_dict = {}
        for term, postings in collection.inverted_index.IDX.items():
            docnos = set(postings)
            for docno in docnos.intersection(weighted_index[term]):
                sum_of_squares_dict.setdefault(docno, 0)

                # Calculate the square of the weight for term 'term' in document 'docno' and add it to the sum of squares
                # w_ln(i, d): Weight of term 'term' in document 'docno' after length normalization
                sum_of_squares_dict[docno] += math.pow(weighted_index[term].get(docno, 0), 2)

        return sum_of_squares_dict

    def print_normalization_time(self, start_time, end_time):
        elapsed_time = end_time - start_time
        print(f"Length Normalization took {elapsed_time} seconds.")
