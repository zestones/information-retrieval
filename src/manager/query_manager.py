from colorama import Fore, Style
from tabulate import tabulate
import math


class QueryManager:
    def __init__(self, collection):
        self.inverted_index = collection.inverted_index
        self.weighted_index = collection.weighted_index
        self.text_processor = collection.text_processor

    def process_query(self, query):
        """
        Processes the query.
        """
        return self.text_processor.pre_processing(query)

    def RSV(self, query):
        document_scores = {}
        query_terms = self.process_query(query)

        # lets remove duplicates
        query_terms = list(set(query_terms))

        for term in query_terms:
            if term in self.weighted_index:
                for docno, score in self.weighted_index[term].items():
                    if docno not in document_scores:
                        document_scores[docno] = 0
                    document_scores[docno] += score

        return sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

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
        headers = ["Docno", "Score"]
        table = []

        for docno, score in results[: 10]:
            table.append([docno, score])

        print(Fore.GREEN + f'Query: {query}' + Style.RESET_ALL)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print()

    def format_query_results(self, query, results, run_id):
        """
        Returns the query results as a list.
        """
        query_results = []
        xml_path = '/article[1]'

        for rank, (docno, score) in enumerate(results[:1500], start=1):
            article_id = docno
            query_results.append((query, 'Q0', article_id, rank, score, run_id, xml_path))

        return query_results
