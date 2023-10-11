import json
import math


class WeightingStrategy:
    def calculate_weight(self, collection):
        raise NotImplementedError("Subclasses must implement this method")

    def IDF(self, collection, term):
        """
        Calculates the IDF of a term.
        """
        # Calculate the IDF
        # idf(i): IDF of term 'term'
        return math.log(collection.collection_size / collection.document_frequency(term))

    def TF(self, collection, docno, term):
        """
        Calculates the TF of a term in a document.
        """
        # Calculate the TF
        # tf(i, d): TF of term 'term' in document 'docno'
        return collection.term_frequency(docno, term)

    def TF_IDF_weight(self, collection, docno, term):
        """
        Returns the tf-idf weight of a term in a document.
        """
        # Calculate the tf-idf weight
        # w(i, d): Weight of term 'term' in document 'docno'
        return (1 + math.log(self.TF(collection, docno, term))) * self.IDF(collection, term)

    def export_weighted_index(self, weighted_index, filename):
        """
        Exports the weighted index to a JSON file.
        """
        weighted_index_data = {"weighted_index": weighted_index}

        # Convert sets to lists for serialization
        weighted_index_data["weighted_index"] = {
            k: {k2: v2 for k2, v2 in v.items()} for k, v in weighted_index_data["weighted_index"].items()}

        with open(filename, "w") as file:
            json.dump(weighted_index_data, file)
