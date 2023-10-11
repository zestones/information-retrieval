import json
import math


class WeightingStrategy:
    def calculate_weight(self, collection):
        raise NotImplementedError("Subclasses must implement this method")

    def TF_IDF_weight(self, collection, docno, term):
        """
        Returns the tf-idf weight of a term in a document.
        """
        tf = collection.term_frequency(docno, term)
        df = collection.document_frequency(term)
        return (1 + math.log(tf)) * math.log(collection.collection_size / df)

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
