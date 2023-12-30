from weighting_strategies.weighting_strategy import WeightingStrategy
import time
import math
import re


class LNUWeighting(WeightingStrategy):
    def __init__(self, slope=1.4):
        self.slope = slope

    def calculate_weight(self, collection):
        """
        Constructs the weighted index using the LNU weighting scheme.
        """
        start_time = time.time()
        weighted_index = {}

        for term, postings in collection.inverted_index.IDX.items():
            for xpath, docno_list in postings.items():
                tag = re.sub(r'\[\d+\]', '', xpath).split("/")[-1]
                avdl = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['avdl'].values[0]

                for docno in docno_list:
                    lnn = 1 + math.log10(collection.term_frequency(docno, term, xpath))
                    length_normalization = 1 + math.log10(collection.document_length(docno, tag) / avdl)

                    pivot = collection.statistics.avg_distinct_terms_in_document
                    nt_d = collection.statistics.distinct_terms_in_document[docno]

                    adjustement = (1 - self.slope) + pivot + (self.slope * nt_d)
                    weight = (lnn / length_normalization) / adjustement

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
        return {"slope": self.slope}
