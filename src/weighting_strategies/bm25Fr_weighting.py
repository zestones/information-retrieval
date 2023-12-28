from weighting_strategies.weighting_strategy import WeightingStrategy

import math
import time
import re
import json


class BM25FrWeighting(WeightingStrategy):
    def __init__(self, k1=1, b=0.5, alpha=1, beta=1, gamma=1):
        self.k1 = k1
        self.b = b

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.ARTICLE = 'article'
        self.ARTICLE_PATH = '/article[1]'

    def calculate_bm25_weight_with_combined_tf(self, collection, term_frequencies):
        """
        Constructs the weighted inverted index using the BM25 weighting scheme.
        """
        weighted_index = {}

        for term, postings in collection.inverted_index.IDX.items():
            for x_path, docno_list in postings.items():
                tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
                N = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['N'].values[0]
                avdl = collection.statistics.avdl_df.loc[collection.statistics.avdl_df['XPath'] == tag]['avdl'].values[0]

                df = collection.document_frequency(term, tag)  # Document frequency
                idf = math.log10((N - df + 0.5) / (df + 0.5))           # Inverse document frequency

                for docno in docno_list:
                    dl = collection.document_length(docno, tag)     # Document length
                    tf = term_frequencies[term][x_path].get(docno, 0)  # Term frequency

                    # Calculate BM25 weight for the term in the document
                    weight = (tf * (self.k1 + 1)) / \
                        (self.k1 * ((1 - self.b) + self.b * (dl / avdl)) + tf)
                    weight *= idf

                    # Update the weighted index
                    if term not in weighted_index:
                        weighted_index[term] = []

                    weighted_index[term].append(
                        {"XPath": self.ARTICLE_PATH, "docno": docno, "weight": weight})

        return weighted_index

    def compute_combined_tf(self, collection):
        """
        Computes the combined term frequency for each term in each document.
        """
        term_frequencies = {}
        for term, postings in collection.inverted_index.TF.items():
            term_frequencies[term] = self.compute_combined_tf_for_term(term, postings, collection)

        return term_frequencies

    def compute_combined_tf_for_term(self, term, postings, collection):
        """
        Computes the combined term frequency for a specific term in different granularities.
        """
        term_freq_for_term = {}
        for x_path, entry in postings.items():
            tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
            term_freq_for_term[x_path] = self.compute_tf_for_granularity(tag, entry)

        combined_term_frequency = self.combine_term_frequency(term_freq_for_term)
        return combined_term_frequency

    def compute_tf_for_granularity(self, granularity, entry):
        """
        Computes the term frequency for a term in a specific granularity.
        """
        tf = 0
        term_freq = {}
        for docno, freq in entry.items():
            if granularity == 'title':
                tf = self.alpha * freq
            elif granularity == 'categories':
                tf = self.beta * freq
            elif granularity == 'bdy':
                tf = self.gamma * freq

            term_freq[docno] = tf

        return term_freq

    def combine_term_frequency(self, term_freq_for_term):
        """
        Combines term frequency for different granularities into a single term frequency.
        """
        combined_tf = {}
        for _, term_freq in term_freq_for_term.items():
            for docno, tf in term_freq.items():
                if self.ARTICLE_PATH not in combined_tf:
                    combined_tf[self.ARTICLE_PATH] = {}

                if docno not in combined_tf[self.ARTICLE_PATH]:
                    combined_tf[self.ARTICLE_PATH][docno] = tf
                else:
                    combined_tf[self.ARTICLE_PATH][docno] += tf

        return combined_tf

    def update_dl(self, collection, term_frequencies):
        """
        We need to compute the document length for each document based on 
        the combined term frequency.
        """
        updated_dl = {}
        for _, postings in term_frequencies.items():
            for granularity, entry in postings.items():
                if granularity == self.ARTICLE_PATH:
                    for docno, freq in entry.items():
                        if docno not in updated_dl:
                            updated_dl[docno] = {self.ARTICLE: 0}
                        updated_dl[docno][self.ARTICLE] += freq

        collection.statistics.document_lengths = updated_dl

        with open('updated_document_lengths.json', 'w') as f:
            json.dump(updated_dl, f)

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

        with open('term_frequencies.json', 'w') as f:
            json.dump(term_frequencies, f)

        self.update_dl(collection, term_frequencies)
        collection.transform_index()

        with open('transformed_index.json', 'w') as f:
            json.dump(collection.inverted_index.IDX, f)

        weighted_index = self.calculate_bm25_weight_with_combined_tf(collection, term_frequencies)
        self.print_computation_time(start_time, time.time())

        return weighted_index
