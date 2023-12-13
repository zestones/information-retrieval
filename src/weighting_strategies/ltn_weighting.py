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
            for xpath, entry in postings.items():
                for docno in entry.get('docno', []):
                    weight = self.TF_IDF_weight(collection, docno, term, xpath)
                    
                    if term not in weighted_index:
                        weighted_index[term] = []
                    
                    weighted_index[term].append({"XPath": xpath, "docno": docno, "weight": weight})
        
        end_time = time.time()
        self.print_computation_time(start_time, end_time)
        
        return weighted_index
