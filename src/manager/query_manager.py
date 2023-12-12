from colorama import Fore, Style
from tabulate import tabulate
import math


class QueryManager:
    def __init__(self, collection):
        self.inverted_index = collection.inverted_index
        self.weighted_index = collection.weighted_index
        self.text_processor = collection.text_processor

        self.QUERY_FILE = '../lib/data/practice_04/topics_M2DSC_7Q.txt'

    def parse_query_file(self, query_file):
        if (query_file is None):
            query_file = self.QUERY_FILE

        parsed_queries = []
        with open(query_file, 'r') as file:
            for line in file:
                if not line.strip():
                    continue
                parts = line.strip().split(' ', 1)

                if len(parts) == 2:
                    query_id, query = parts
                    parsed_queries.append((query_id, query))

        return parsed_queries

    def launch_query(self, query_id, query):
        res = self.RSV(query)
        res = self.remove_overlapping_paths(res)
        query_results = self.format_query_results(query_id, res, "BengezzouIdrissMezianeGhilas")

        return query_results

    def process_query(self, query):
        """
        Processes the query.
        """
        return self.text_processor.pre_processing(query)

    def RSV(self, query):
        document_scores = {}
        query_terms = self.process_query(query)

        # Remove duplicates from query_terms
        query_terms = list(set(query_terms))

        for term in query_terms:
            if term in self.weighted_index:
                for entry in self.weighted_index[term]:
                    docno = entry['docno']
                    xpath = entry['XPath']
                    score = entry['weight']

                    # Accumulate scores only if term occurs in the same document and XPath
                    doc_xpath_key = (docno, xpath)
                    if doc_xpath_key not in document_scores:
                        document_scores[doc_xpath_key] = 0
                    document_scores[doc_xpath_key] += score

        sorted_document_scores = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_document_scores

    def remove_overlapping_paths(self, sorted_document_scores):
        # Dictionary to store the deepest paths for each document
        deepest_paths = {}
        non_overlapping_scores = {}

        for doc_xpath, score in sorted_document_scores:
            docno, xpath = doc_xpath

            # Check if there's already a recorded deepest path for this document
            if docno not in deepest_paths:
                deepest_paths[docno] = xpath
                non_overlapping_scores[docno] = score
            else:
                existing_xpath = deepest_paths[docno]

                # Check if the current XPath is a subpath of the existing XPath
                if xpath.startswith(existing_xpath + '/') or xpath == existing_xpath:
                    # If the score is higher, update the score and the deepest path
                    if score >= non_overlapping_scores[docno]:
                        non_overlapping_scores[docno] = score
                        deepest_paths[docno] = xpath
                else:
                    # If the current path is not a subpath, consider it as a non-overlapping path
                    if score >= non_overlapping_scores[docno]:
                        non_overlapping_scores[docno] = score
                        deepest_paths[docno] = xpath

        # Construct the non-overlapping list of scores
        non_overlapping_scores_list = [((docno, deepest_paths[docno]), score)
                                       for docno, score in non_overlapping_scores.items()]

        # Sort the non-overlapping scores
        sorted_non_overlapping_scores = sorted(
            non_overlapping_scores_list, key=lambda x: x[1], reverse=True)

        return sorted_non_overlapping_scores

    def normalize_query(self, query):
        """
        Normalizes the query.
        """
        query_terms = self.process_query(query)
        query_length = math.sqrt(sum([math.pow(1, 2) for _ in query_terms]))
        query_weights = {}

        for term in query_terms:
            query_weights[term] = 1 / query_length

        return query_terms, query_weights

    def cosine_similarity(self, query):
        """
        Evaluates the query using the ltc weighting scheme.
        """
        query_terms, query_weights = self.normalize_query(query)

        document_scores = {}
        for term in query_terms:
            if term in self.weighted_index:
                for docno, _ in self.weighted_index[term].items():
                    wln = self.weighted_index[term][docno]

                    # Calcul du produit wln(i, d) * qln(i)
                    product = wln * query_weights[term]

                    # Ajout du produit au score du document
                    if (docno not in document_scores):
                        document_scores[docno] = 0

                    document_scores[docno] += product

        sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_documents

    def print_query_results(self, query, results):
        """
        Prints the query results inside a table.
        """
        headers = ["Docno", "Score", "XPath"]
        table = []

        for entry, score in results[: 10]:
            docno, xpath = entry
            table.append([docno, xpath, score])

        print(Fore.GREEN + f'Query: {query}' + Style.RESET_ALL)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print()

    def format_query_results(self, query, results, run_id):
        """
        Returns the query results as a list.
        """
        query_results = []
        for rank, (docno, score) in enumerate(results[:1500], start=1):
            article_id, xpath = docno
            query_results.append((query, 'Q0', article_id, rank, score, run_id, xpath))

        return query_results
