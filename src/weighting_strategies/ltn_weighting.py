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
            for xpath, docno_list in postings.items():
                for docno in docno_list:
                    weight = self.TF_IDF_weight(collection, docno, term, xpath)

                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append({"XPath": xpath, "docno": docno, "weight": weight})

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index

    def get_weighting_scheme_parameters(self):
        """
        Returns the parameters of the weighting scheme.
        """
        return {}
