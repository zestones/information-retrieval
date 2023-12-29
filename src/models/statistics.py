import pandas as pd
import json


class Statistics:
    def __init__(self, inverted_index, export_statistics: bool = False) -> None:
        """
        Initializes the Statistics class.

        Args:
            inverted_index (object): Object class containing data about IDX, TF ect..
            export_statistics (bool, optional): Flag to export statistics. Defaults to False.
        """
        self.RESOURCES_FOLDER = '../docs/resources/'  # Resources folder to save the stats

        self.avg_term_lengths_in_collection = 0    # Average term length in the collection
        self.collection_vocabulary_sizes = 0       # Number of unique terms in the collection
        self.collection_frequency_of_terms = 0     # Number of times a term appears in the collection
        self.indexing_time = 0                     # Time to index the collection

        # Dataframe to store the average document length and document length of each XPath and document
        self.avdl_df = pd.DataFrame(columns=['XPath', 'N', 'avdl', 'number_of_words'])
        self.document_lengths = {}          # {docno: {XPath: dl}}

        self.export_statistics = export_statistics
        self.inverted_index = inverted_index

        self.compute_statistics()
        if self.export_statistics:
            self.export_stats()

    def _compute_document_length(self, docno, x_path, number_of_words):
        """
        Computes the document length of the document.

        Args:
            docno (str): Document number.
            x_path (str): XPath of the document.
            number_of_words (int): Number of words in the document.
        """
        if docno not in self.document_lengths:
            self.document_lengths[docno] = {x_path: number_of_words}
        else:
            if x_path not in self.document_lengths[docno]:
                self.document_lengths[docno][x_path] = number_of_words

            self.document_lengths[docno][x_path] += number_of_words

    def _compute_average_document_length(self, x_path, n, number_of_words):
        """
        Computes the average document length.

        Args:
            x_path (str): XPath of the document.
            n (int): Number of documents.
            number_of_words (int): Number of words in the document.
        """
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

    def _compute_collection_frequencies(self):
        """
        Calculate collection frequency of terms.
        TOFIX : This function is not used and does not work.
        """
        for term, entries in self.inverted_index.TF.items():
            frequency = 0
            for xpath, entry in entries.items():
                frequency += sum(self.term_frequency(docno, term, xpath)
                                 for docno, _ in entry.items())

        self.collection_frequencies[term] = frequency

    def compute_statistics(self):
        """
        Computes the statistics for the parsed documents.
        """
        vocabulary = set()
        new_rows = []

        for docno, data in self.inverted_index.parsed_documents.items():
            for x_path in data.keys():
                number_of_words = len(data[x_path]["terms"])
                N = data[x_path]["N"]
                vocabulary.update(data[x_path]["terms"])

                self._compute_document_length(docno, x_path, number_of_words)
                self._compute_average_document_length(x_path, N, number_of_words)

        if new_rows:
            new_data = pd.DataFrame(new_rows)
            self.dl_df = pd.concat([self.dl_df, new_data], ignore_index=True)

        # compute the average document length
        self.avdl_df['avdl'] = self.avdl_df['number_of_words'] / self.avdl_df['N']
        self.collection_vocabulary_sizes = len(vocabulary)

        # self.collection_frequency_of_terms = sum(list(self.collection_frequencies.values()))

    def export_stats(self):
        """
        Exports the computed statistics to files.
        """
        stats = {
            'indexing_time': self.indexing_time,
            'avg_collection_lengths': None,
            'avg_term_lengths_in_collection': self.avg_term_lengths_in_collection,
            'collection_vocabulary_sizes': self.collection_vocabulary_sizes,
            'collection_frequency_of_terms': self.collection_frequency_of_terms,
        }

        avg_collection_lengths = self.avdl_df.loc[self.avdl_df['XPath'] == './/article']['avdl'].values
        if len(avg_collection_lengths) > 0:
            stats['avg_collection_lengths'] = avg_collection_lengths[0]

        with open(self.RESOURCES_FOLDER + "statistics.json", 'w') as outfile:
            json.dump(stats, outfile, indent=4)

        with open(self.RESOURCES_FOLDER + 'dl.json', 'w') as outfile:
            json.dump(self.document_lengths, outfile, indent=4)

        # write the dataframe to a file
        self.avdl_df.to_csv(self.RESOURCES_FOLDER + 'avdl.csv', index=False)
