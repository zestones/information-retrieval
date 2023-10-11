from weighting_strategies.weighting_strategy import WeightingStrategy


class LTNWeighting(WeightingStrategy):
    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index.
        """
        weighted_index = {}
        for term, postings in collection.inverted_index.IDX.items():
            weighted_index[term] = {}
            for docno in postings:
                weighted_index[term][docno] = self.TF_IDF_weight(collection, docno, term)
        return weighted_index
