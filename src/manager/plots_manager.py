import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


class PlotsManager:
    def __init__(self, collections_manager) -> None:

        self.collections_manager = collections_manager
        self.RESSOURCES_FOLDER = self.collections_manager.RESOURCES_FOLDER

        self.__xlabel = 'Collection Size'
        self.collection_sizes = [
            collection.collection_size for collection in self.collections_manager.collections]

    def plot(self, title, xlabel, ylabel, xdata, ydata, filename):
        """
        Plot a graph.
        """
        plt.figure(figsize=(10, 6))

        # Plot the data points with markers and lines
        plt.plot(xdata, ydata, marker='o', linestyle='-', label='Data Points')

        # Set the title and axis labels
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        # Enable the grid
        plt.grid(True)

        # Save the plot to a file
        plt.savefig(self.RESSOURCES_FOLDER + filename)

        # Show the plot
        plt.show()

    def plot_indexing_time_by_collection_size(self):
        """
        Display efficiency for all collections.
        """
        ylabel = 'Time (seconds)'
        filename = 'indexing_time_by_collection_size.png'
        ydata = self.collections_manager.indexing_times
        self.plot('Indexing Time by Collection Size', self.__xlabel,
                  ylabel, self.collection_sizes, ydata, filename)

    def plot_document_length_evolution(self):
        """
        Plot the evolution of document length as the collection size grows.
        """
        ylabel = 'Average Document Length'
        filename = 'document_length_evolution.png'
        ydata = [collection.collection_statistics.avg_collection_lengths for collection in self.collections_manager.collections]
        self.plot('Document Length Evolution', self.__xlabel,
                  ylabel, self.collection_sizes, ydata, filename)

    def plot_term_length_evolution(self):
        """
        Plot the evolution of term length as the collection size grows.
        """
        ylabel = 'Average Term Length'
        filename = 'term_length_evolution.png'
        ydata = [collection.collection_statistics.avg_term_lengths_in_collection for collection in self.collections_manager.collections]
        self.plot('Term Length Evolution', self.__xlabel,
                  ylabel, self.collection_sizes, ydata, filename)

    def plot_vocabulary_size_evolution(self):
        """
        Plot the evolution of vocabulary size as the collection size grows.
        """
        ylabel = 'Vocabulary Size'
        filename = 'vocabulary_size_evolution.png'
        ydata = [collection.collection_statistics.collection_vocabulary_sizes for collection in self.collections_manager.collections]
        self.plot('Vocabulary Size Evolution', self.__xlabel,
                  ylabel, self.collection_sizes, ydata, filename)

    def plot_collection_frequency_of_terms_evolution(self):
        """
        Plot the evolution of collection frequency of terms as the collection size grows.
        """
        collection_frequencies = [
            collection.collection_statistics.collection_frequency_of_terms for collection in self.collections_manager.collections]

        plt.figure(figsize=(50, 20))
        for i in range(len(self.collections_manager.collections)):
            plt.bar(
                self.collection_sizes[i],
                collection_frequencies[i],
                label=self.collections_manager.collections[i].label,
                alpha=1
            )

            # Ajouter une annotation textuelle avec la valeur exacte
            plt.text(self.collection_sizes[i], collection_frequencies[i], str(
                collection_frequencies[i]), ha='center', va='bottom')

        plt.title('Collection Frequency of Terms Evolution')
        plt.xlabel(self.__xlabel)
        plt.ylabel('Collection Frequency of Terms')
        plt.legend()

        # Activer le quadrillage
        plt.grid(True)

        plt.savefig(self.RESSOURCES_FOLDER + 'collection_frequency_of_terms_evolution.png')
        plt.show()
