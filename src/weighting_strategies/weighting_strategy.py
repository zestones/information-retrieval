from colorama import Fore, Style
import json
import math
import re


class WeightingStrategy:
    def calculate_weight(self, collection):
        raise NotImplementedError("Subclasses must implement this method")

    def IDF(self, collection, term, x_path):
        """
        Calculates the IDF of a term.
        """
        # Calculate the IDF
        # idf(i): IDF of term 'term'
        tag = re.sub(r'\[\d+\]', '', x_path).split("/")[-1]
        return math.log10(collection.collection_size / collection.document_frequency(term, tag))

    def TF(self, collection, docno, term, x_path):
        """
        Calculates the TF of a term in a document.
        """
        # Calculate the TF
        # tf(i, d): TF of term 'term' in document 'docno', at XPath 'x_path'
        return collection.term_frequency(docno, term, x_path)

    def TF_IDF_weight(self, collection, docno, term, x_path):
        """
        Returns the tf-idf weight of a term in a document.
        """
        # Calculate the tf-idf weight
        # w(i, d): Weight of term 'term' in document 'docno'
        return (1 + math.log10(self.TF(collection, docno, term, x_path))) * self.IDF(collection, term, x_path)

    def export_weighted_index(self, weighted_index, filename):
        """
        Exports the weighted index to a JSON file.
        """
        weighted_index_data = {"weighted_index": weighted_index}

        with open(filename, "w") as file:
            json.dump(weighted_index_data, file)

    def print_computation_time(self, start_time, end_time):
        """
        Prints the computation time.
        """
        print(Fore.YELLOW + "> Weighting time: " + str(end_time
              - start_time) + " seconds" + Style.RESET_ALL, end="\n\n")

    def get_weighting_scheme_parameters(self):
        """
        Returns the parameters of the weighting scheme.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def get_weighting_scheme_name(self):
        """
        Returns the name of the weighting scheme.
        """
        return self.__class__.__name__.replace("Weighting", "").lower()
