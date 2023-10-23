from weighting_strategies.weighting_strategy import WeightingStrategy

import time

class LTNWeighting(WeightingStrategy):
    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index.
        """
        start_time = time.time()
        weighted_index = {}

        for term, postings in collection.inverted_index.IDX.items():
            weighted_index[term] = {}
            for docno in postings:
                weighted_index[term][docno] = self.TF_IDF_weight(collection, docno, term)
        
        end_time = time.time()
        self.print_computation_time(start_time, end_time)
        
        return weighted_index
