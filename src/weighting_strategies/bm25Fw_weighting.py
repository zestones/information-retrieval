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

        self.granularity = [".//title", ".//body", ".//categories"]

    def compute_bm25_weight_on_fields(self, collection):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}

        for term, postings in collection.inverted_index.IDX.items():
            for granularity, entry in postings.items():
                N = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == granularity]['N'].values[0]
                avdl = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == granularity]['avdl'].values[0]

                df = collection.document_frequency(term, granularity)    # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))            # Inverse document frequency

                if granularity in self.granularity:
                    for docno, x_path in entry.items():
                        dl = collection.document_length(docno, granularity)       # Document length
                        tf = collection.term_frequency(docno, term, granularity)  # Term frequency

                        # Calculate BM25 weight for the term in the document
                        weight = (tf * (self.k1 + 1)) / \
                            (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                        weight *= idf

                        # Update the weighted index
                        if term not in weighted_index:
                            weighted_index[term] = []

                        weighted_index[term].append({"XPath": x_path, "docno": docno, "weight": weight})

        return weighted_index

    def remove_duplicates(self, weighted_index):
        for term, postings in weighted_index.items():
            # inside a posting list, sum the weights of the same docno
            unique_postings = []
            for entry in postings:
                if not any(e["docno"] == entry["docno"] for e in unique_postings):
                    entry["weight"] = sum([e["weight"]
                                          for e in postings if e["docno"] == entry["docno"]])
                    unique_postings.append(entry)
            weighted_index[term] = unique_postings

        return weighted_index

    def combine_weights(self, weighted_index):
        # Combine the weights of the different fields with alpha and beta factors
        article_weights = {term: [] for term in set(weighted_index["title"].keys())
                           .union(weighted_index["body"].keys())
                           .union(weighted_index["abstract"].keys())
                           }

        for term in article_weights.keys():
            for field in ["title", "body", "abstract"]:
                for entry in weighted_index[field].get(term, []):
                    docno = entry["docno"]
                    weight = entry["weight"]

                    if docno not in article_weights[term]:
                        article_weights[term].append(
                            {"XPath": "/article[1]", "docno": docno, "weight": 0})

                    if field == "title":
                        article_weights[term][-1]["weight"] += self.alpha * weight

                    elif field == "abstract":
                        article_weights[term][-1]["weight"] += self.beta * weight

                    elif field == "body":
                        article_weights[term][-1]["weight"] += self.gamma * weight

        return article_weights

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

        with open("weighted_index.json", "w") as f:
            json.dump(weighted_index, f)

        exit()

        weighted_index = self.combine_weights(weighted_index)
        weighted_index = self.remove_duplicates(weighted_index)

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index
