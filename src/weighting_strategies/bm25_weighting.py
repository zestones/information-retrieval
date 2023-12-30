from weighting_strategies.weighting_strategy import WeightingStrategy

import math
import time
import json
import re


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

        for term, postings in collection.inverted_index.IDX.items():
            for x_path, docno_list in postings.items():
                tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
                N = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['N'].values[0]
                avdl = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['avdl'].values[0]

                df = collection.document_frequency(term, tag)          # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))          # Inverse document frequency
                for docno in docno_list:
                    dl = collection.document_length(docno, tag)  # Document lengt
                    tf = collection.term_frequency(docno, term, x_path)

                    # Calculate BM25 weight for the term in the document
                    weight = (tf * (self.k1 + 1)) / \
                        (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                    weight *= idf

                    # Update the weighted index
                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append({"XPath": x_path, "docno": docno, "weight": weight})

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index

    def get_weighting_scheme_parameters(self):
        """
        Returns the parameters of the weighting scheme.
        """
        return {"k": self.k1, "b": self.b}
