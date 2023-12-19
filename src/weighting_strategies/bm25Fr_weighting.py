from weighting_strategies.weighting_strategy import WeightingStrategy

import math
import time
import re


class BM25FrWeighting(WeightingStrategy):
    def __init__(self, k1=1, b=0.5, alpha=1, beta=1, gamma=1):
        self.k1 = k1
        self.b = b

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def calculate_bm25_weight_with_combined_tf(self, collection, term_frequencies):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}
        start_time = time.time()

        N = collection.collection_size                       # Total number of documents in the collection
        avdl = collection.statistics.avg_collection_lengths  # Average document length in the collection

        for term, postings in collection.inverted_index.IDX.items():
            for x_path, entry in postings.items():

                df = collection.document_frequency(term, x_path)    # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))       # Inverse document frequency

                for docno in entry.get('docno', []):
                    dl = collection.document_length(docno)
                    tf = term_frequencies[term]['/article[1]'].get(docno, 0)  # Term frequency

                    # Calculate BM25 weight for the term in the document
                    weight = (tf * (self.k1 + 1)) / \
                        (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                    weight *= idf

                    # Update the weighted index
                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append(
                        {"XPath": '/article[1]', "docno": docno, "weight": weight})

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index

    def compute_combined_tf(self, collection):
        """
        Computes the combined term frequency for each term in each document.
        """
        term_frequencies = {}
        for term, postings in collection.inverted_index.IDX.items():
            term_frequencies[term] = {}

            for x_path, entry in postings.items():
                # Get the last element of the XPath
                element = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
                tf = 0
                for docno in entry.get('docno', []):
                    # Compute the combined term frequency
                    if element == 'title':
                        tf += self.alpha * collection.term_frequency(docno, term, x_path)
                    elif element == 'categories':
                        tf += self.beta * collection.term_frequency(docno, term, x_path)
                    elif element == 'bdy':
                        tf += self.gamma * collection.term_frequency(docno, term, x_path)

                    # Update the term frequency
                    if '/article[1]' not in term_frequencies[term]:
                        term_frequencies[term]['/article[1]'] = {}

                    if docno not in term_frequencies[term]['/article[1]']:
                        term_frequencies[term]['/article[1]'].update({docno: tf})
                    else:
                        term_frequencies[term]['/article[1]'][docno] += tf

        return term_frequencies

    def calculate_weight(self, collection):
        """
        Constructs the weighted inverted index using the BM25Fr weighting scheme.
        BM25Fr (Roberston, 2004) is a variant of BM25 with an early combination on the frequency 
        of a term and the values alpha, beta and gamma.

        The BM25Fr weighting scheme is defined as follows:
        1. tf combination:
        tf'(t, article) = alpha * tf(t, title) + beta * tf(t, abstract) + gamma * tf(t, body)

        2. compute the BM25 weight with tf'(t, article) and df(t)
        """
        start_time = time.time()
        weighted_index = {}
        term_frequencies = self.compute_combined_tf(collection)
        collection.transform_index()

        weighted_index = self.calculate_bm25_weight_with_combined_tf(collection, term_frequencies)

        end_time = time.time()
        self.print_computation_time(start_time, end_time)

        return weighted_index
