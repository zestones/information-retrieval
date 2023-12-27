import pandas as pd
import statistics
import json


class Statistics:
    def __init__(self, collection, export_statistics: bool = False) -> None:
        self.collection = collection
        self.RESOURCES_FOLDER = '../docs/resources/'  # Resources folder to save the stats

        self.avg_term_lengths_in_collection = 0    # Average term length in the collection
        self.collection_vocabulary_sizes = 0       # Number of unique terms in the collection
        self.collection_frequency_of_terms = 0     # Number of times a term appears in the collection

        # Dataframe to store the average document length and document length of each XPath and document
        self.avdl_df = pd.DataFrame(columns=['XPath', 'N', 'avdl', 'number_of_words'])
        self.document_lengths = {}          # {docno: {XPath: dl}}

        self.calculate_statistics()
        if (export_statistics):
            self.export_stats(f'stats-{self.collection.label}.json')

    def compute_document_length(self, docno, x_path, number_of_words):
        """
        Computes the document length of the document.
        """
        if docno not in self.document_lengths:
            self.document_lengths[docno] = {x_path: number_of_words}
        else:
            if x_path not in self.document_lengths[docno]:
                self.document_lengths[docno][x_path] = number_of_words

            self.document_lengths[docno][x_path] += number_of_words

    def compute_average_document_length(self, x_path, n, number_of_words):
        if x_path in self.avdl_df['XPath'].values:
            self.avdl_df.loc[self.avdl_df['XPath'] == x_path, 'N'] += n
            self.avdl_df.loc[
                self.avdl_df['XPath'] == x_path, 'number_of_words'] += number_of_words
        else:
            self.avdl_df = pd.concat([self.avdl_df, pd.DataFrame({
                'XPath': [x_path],
                'N': [n],
                'number_of_words': [number_of_words]
            })], ignore_index=True)

    def calculate_statistics(self):
        """
        """
        vocabulary = set()
        new_rows = []

        for docno, data in self.collection.document_parser.parsed_documents.items():
            for x_path in data.keys():
                number_of_words = len(data[x_path]["terms"])
                N = data[x_path]["N"]
                vocabulary.update(data[x_path]["terms"])

                self.compute_document_length(docno, x_path, number_of_words)
                self.compute_average_document_length(x_path, N, number_of_words)

        if new_rows:
            new_data = pd.DataFrame(new_rows)
            self.dl_df = pd.concat([self.dl_df, new_data], ignore_index=True)

        # compute the average document length
        self.avdl_df['avdl'] = self.avdl_df['number_of_words'] / self.avdl_df['N']
        self.collection_vocabulary_sizes = len(vocabulary)

        self.collection_frequency_of_terms = sum(list(self.collection.collection_frequencies.values()))

    def export_stats(self, filename):
        """
        Exports all the statistics to a JSON file.
        """
        stats = {
            'indexing_time': self.collection.inverted_index.indexing_time,
            'avg_collection_lengths': None,
            'avg_term_lengths_in_collection': self.avg_term_lengths_in_collection,
            'collection_vocabulary_sizes': self.collection_vocabulary_sizes,
            'collection_frequency_of_terms': self.collection_frequency_of_terms,
        }

        avg_collection_lengths = self.avdl_df.loc[self.avdl_df['XPath'] == './/article']['avdl'].values
        if len(avg_collection_lengths) > 0:
            stats['avg_collection_lengths'] = avg_collection_lengths[0]

        with open(self.RESOURCES_FOLDER + filename, 'w') as outfile:
            json.dump(stats, outfile, indent=4)

        with open(self.RESOURCES_FOLDER + 'dl.json', 'w') as outfile:
            json.dump(self.document_lengths, outfile, indent=4)

        # write the dataframe to a file
        self.avdl_df.to_csv(self.RESOURCES_FOLDER + 'avdl.csv', index=False)
