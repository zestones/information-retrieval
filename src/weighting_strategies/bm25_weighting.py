from weighting_strategies.weighting_strategy import WeightingStrategy

import math


class BM25Weighting(WeightingStrategy):
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b

    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}

        N = collection.collection_size  # Total number of documents in the collection
        avdl = collection.statistics.avg_collection_lengths  # Average document length in the collection
        for term, postings in collection.inverted_index.IDX.items():
            df = len(postings)  # Document frequency of the term
            idf = math.log((N - df + 0.5) / (df + 0.5))  # Inverse document frequency

            for docno in postings:
                # Document length
                dl = collection.document_length(docno)
                tf = collection.term_frequency(docno, term)

                # Calculate BM25 weight for the term in the document
                weight = (tf * (self.k1 + 1)) / \
                    (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                weight *= idf

                # Update the weighted index
                if term not in weighted_index:
                    weighted_index[term] = {}
                weighted_index[term][docno] = weight

        return weighted_index
