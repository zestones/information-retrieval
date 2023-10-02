import matplotlib.pyplot as plt


class PlotsManager:
    def __init__(self, collections_manager) -> None:
        self.collections_manager = collections_manager
        self.RESSOURCES_FOLDER = self.collections_manager.RESOURCES_FOLDER

        self.__xlabel = 'Collection Size'

    def plot_indexing_time_by_collection_size(self):
        """
        Display efficiency for all collections.
        """
        plt.figure(figsize=(10, 6))

        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections_manager.collections]
        plt.plot(collection_sizes, self.collections_manager.indexing_times, marker='o', linestyle='-')

        plt.title('Indexing Time by Collection Size')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Time (seconds)')

        plt.xticks(collection_sizes)
        plt.yticks(self.collections_manager.indexing_times)

        plt.grid(True)

        plt.savefig(self.RESSOURCES_FOLDER + 'indexing_time_by_collection_size.png')
        plt.show()

    def plot_document_length_evolution(self):
        """
        Plot the evolution of document length as the collection size grows.
        """
        plt.figure(figsize=(10, 6))

        for collection in self.collections_manager.collections:
            collection_sizes = [
                collection.collection_statistics.collection_size] * len(collection.collection_statistics.document_lengths)

            document_lengths = collection.collection_statistics.document_lengths

            plt.plot(collection_sizes, document_lengths, marker='o',
                     linestyle='-', label=collection.label)

        plt.title('Document Length Evolution')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Document Length')
        plt.grid(True)
        plt.legend()

        plt.savefig(self.RESSOURCES_FOLDER + 'document_length_evolution.png')
        plt.show()

    def plot_term_length_evolution(self):
        """
        Plot the evolution of term length as the collection size grows.
        """
        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections_manager.collections]
        term_lengths = [
            collection.collection_statistics.term_lengths_in_collection for collection in self.collections_manager.collections]

        plt.figure(figsize=(50, 20))
        for i in range(len(self.collections_manager.collections)):
            plt.bar(
                collection_sizes[i],
                term_lengths[i],
                label=self.collections_manager.collections[i].label,
                alpha=1
            )

        plt.title('Term Length Evolution')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Term Length')
        plt.legend()

        plt.text(collection_sizes[i], term_lengths[i], str(
            term_lengths[i]), ha='center', va='bottom')

        plt.savefig(self.RESSOURCES_FOLDER + 'term_length_evolution.png')
        plt.show()

    def plot_vocabulary_size_evolution(self):
        """
        Plot the evolution of vocabulary size as the collection size grows.
        """
        plt.figure(figsize=(10, 6))

        for collection in self.collections_manager.collections:
            collection_sizes = [
                collection.collection_statistics.collection_size] * len(collection.collection_statistics.documents_vocabulary_sizes)

            vocabulary_sizes = collection.collection_statistics.documents_vocabulary_sizes

            plt.plot(collection_sizes, vocabulary_sizes, marker='o',
                     linestyle='-', label=collection.label)

        plt.title('Vocabulary Size Evolution')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Vocabulary Size')
        plt.grid(True)
        plt.legend()

        plt.savefig(self.RESSOURCES_FOLDER + 'vocabulary_size_evolution.png')
        plt.show()

    def plot_collection_frequency_of_terms_evolution(self):
        """
        Plot the evolution of collection frequency of terms as the collection size grows.
        """
        collection_sizes = [
            collection.collection_statistics.collection_size for collection in self.collections_manager.collections]
        collection_frequencies = [
            collection.collection_statistics.collection_frequency_of_terms for collection in self.collections_manager.collections]

        plt.figure(figsize=(50, 20))
        for i in range(len(self.collections_manager.collections)):
            plt.bar(
                collection_sizes[i],
                collection_frequencies[i],
                label=self.collections_manager.collections[i].label,
                alpha=1
            )

            # Ajouter une annotation textuelle avec la valeur exacte
            plt.text(collection_sizes[i], collection_frequencies[i], str(
                collection_frequencies[i]), ha='center', va='bottom')

        plt.title('Collection Frequency of Terms Evolution')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Collection Frequency of Terms')
        plt.legend()

        # Activer le quadrillage
        plt.grid(True)

        plt.savefig(self.RESSOURCES_FOLDER + 'collection_frequency_of_terms_evolution.png')
        plt.show()
