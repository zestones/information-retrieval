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

    def evaluate_query(self, query):
        """
        Evaluates the query using the weighted index.
        """
        document_scores = {}
        query_terms = self.process_query(query)

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

    def evaluate_ltc_query(self, query):
        """
        Evaluates the query using the ltc weighting scheme.
        """
        query_terms, query_weights = self.normalize_query(query)
        print("Query terms:", query_terms)
        print("Query weights:", query_weights)

        # print a part of the weighted_index
        print("Weighted index:", self.weighted_index)

        document_scores = {}
        for term in query_terms:
            if term in self.weighted_index:
                for docno, _ in self.weighted_index[term].items():
                    wln = self.weighted_index[term][docno]

                    print("wln(i, d):", wln)
                    print("qln(i):", query_weights[term])
                    # Calcul du produit wln(i, d) * qln(i)
                    product = wln * query_weights[term]

                    # Ajout du produit au score du document
                    document_scores[docno] += product

        # Triez les documents en fonction de leur score de similarité cosinus
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
