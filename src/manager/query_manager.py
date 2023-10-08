from colorama import Fore, Style
from tabulate import tabulate


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

    def print_query_results(self, query, results):
        """
        Prints the query results inside a table.
        """
        headers = ["Docno", "Score"]
        table = []

        for docno, score in results[:10]:
            table.append([docno, score])

        print(Fore.GREEN + f'Query: {query}' + Style.RESET_ALL)
        print(tabulate(table, headers=headers, tablefmt="fancy_grid"))
        print()
