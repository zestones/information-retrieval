import pandas as pd
import statistics
import json


class Statistics:
    def __init__(self, collection, export_statistics: bool = False) -> None:
        self.collection = collection  # TODO : extend the Statistics class
        self.RESOURCES_FOLDER = '../docs/resources/'  # Resources folder to save the stats

        self.avg_term_lengths_in_collection = 0    # Average term length in the collection
        self.collection_vocabulary_sizes = 0       # Number of unique terms in the collection
        self.collection_frequency_of_terms = 0     # Number of times a term appears in the collection

        # define a dataframe to store the statistics
        self.avdl_df = pd.DataFrame(columns=['XPath', 'N', 'avdl', 'number_of_words'])

        self.calculate_statistics()
        if (export_statistics):
            self.export_stats(f'stats-{self.collection.label}.json')

    def calculate_statistics(self):
        """
        """
        vocabulary = set()
        for _, data in self.collection.document_parser.parsed_documents.items():
            for x_path in data.keys():
                number_of_words = len(data[x_path]["terms"])
                N = data[x_path]["N"]
                vocabulary.update(data[x_path]["terms"])

                # check if x_path is in the dataframe and update the values
                if x_path in self.avdl_df['XPath'].values:
                    self.avdl_df.loc[self.avdl_df['XPath'] == x_path, 'N'] += N
                    self.avdl_df.loc[
                        self.avdl_df['XPath'] == x_path, 'number_of_words'] += number_of_words
                else:
                    # add the x_path to the dataframe
                    self.avdl_df = pd.concat([self.avdl_df, pd.DataFrame({
                        'XPath': [x_path],
                        'N': [N],
                        'number_of_words': [number_of_words]
                    })], ignore_index=True)

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
            'avg_collection_lengths': self.avdl_df.loc[self.avdl_df['XPath'] == './/article']['avdl'].values[0],
            'avg_term_lengths_in_collection': self.avg_term_lengths_in_collection,
            'collection_vocabulary_sizes': self.collection_vocabulary_sizes,
            'collection_frequency_of_terms': self.collection_frequency_of_terms,
        }

        with open(self.RESOURCES_FOLDER + filename, 'w') as outfile:
            json.dump(stats, outfile, indent=4)

        # write the dataframe to a file
        self.avdl_df.to_csv(self.RESOURCES_FOLDER + 'avdl.csv', index=False)
