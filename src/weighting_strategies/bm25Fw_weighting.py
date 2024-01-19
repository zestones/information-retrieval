from weighting_strategies.weighting_strategy import WeightingStrategy

import math
import time
import re
import json


class BM25FwWeighting(WeightingStrategy):
    def __init__(self, k1=1, b=0.5, alpha=1, beta=1, gamma=1):
        self.k1 = k1
        self.b = b

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.ALPHA_GRANULARITY = 'title'
        self.BETA_GRANULARITY = 'categories'
        self.GAMMA_GRANULARITY = 'body'

    def compute_bm25_weight_on_fields(self, collection):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}

        for term, postings in collection.inverted_index.IDX.items():
            for x_path, docno_list in postings.items():
                tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
                N = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['N'].values[0]
                avdl = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['avdl'].values[0]

                df = collection.document_frequency(term, tag)            # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))            # Inverse document frequency

                for docno in docno_list:
                    dl = collection.document_length(docno, tag)               # Document length
                    tf = collection.term_frequency(docno, term, x_path)  # Term frequency

                    # Calculate BM25 weight for the term in the document
                    weight = (tf * (self.k1 + 1)) / \
                        (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                    weight *= idf

                    # Update the weighted index
                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append({"XPath": x_path, "docno": docno, "weight": weight})

        return weighted_index

    def _apply_weights_factor(self, weighted_index):
        for _, postings in weighted_index.items():
            for posting in postings:
                tag = re.sub(r'\[\d+\]', '', posting["XPath"]).split("/")[-1]
                if tag == self.ALPHA_GRANULARITY:
                    posting["weight"] *= self.alpha
                elif tag == self.BETA_GRANULARITY:
                    posting["weight"] *= self.beta
                elif tag == self.GAMMA_GRANULARITY:
                    posting["weight"] *= self.gamma

        return weighted_index

    def _sum_weights(self, weighted_index):
        weighted_index_combined = {}
        for term, postings in weighted_index.items():
            if term not in weighted_index_combined:
                weighted_index_combined[term] = {}

            for posting in postings:
                docno = posting["docno"]
                weight = posting["weight"]

                if docno not in weighted_index_combined[term]:
                    weighted_index_combined[term][docno] = weight
                else:
                    weighted_index_combined[term][docno] += weight

        result = {}
        for term, postings in weighted_index_combined.items():
            result[term] = [{"XPath": "/article[1]", "docno": docno, "weight": weight} for docno, weight in postings.items()]

        return result

    def combine_weights(self, weighted_index):
        # first step: apply the alpha, beta, gamma weights to the weights of the different fields
        # second step: sum the weights of the different fields by term and docno in a new XPaths field ("/article[1]")

        weighted_index = self._apply_weights_factor(weighted_index)
        weighted_index = self._sum_weights(weighted_index)

        return weighted_index

    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index using the BM25Fw weighting scheme.
        BM25Fw (Wilkinson94) is a variant of BM25 with a late combination of the weights
        of the different fields with alpha and beta factors.

        The BM25Fw weighting scheme is defined as follows:
        w(d, t) = BM25(tf(t, d), df(t))
        where:
        w(t, d, article) = alpha * w(t, d, title) + beta * w(t, d, body) + gamma * w(t, d, abstract) 
        """
        start_time = time.time()

        weighted_index = {}
        weighted_index = self.compute_bm25_weight_on_fields(collection)
        weighted_index = self.combine_weights(weighted_index)

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index

    def get_weighting_scheme_parameters(self):
        """
        Returns the parameters of the weighting scheme.
        """
        return {"k": self.k1, "b": self.b, "alpha": self.alpha, "beta": self.beta, "gamma": self.gamma}
