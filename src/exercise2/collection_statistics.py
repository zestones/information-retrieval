import statistics
import matplotlib.pyplot as plt

class CollectionStatistics:
    def __init__(self, collection):
        self.collection = collection 
        
        self.collection_size = 0  
        self.document_lengths = [] 
        self.term_lengths = [] 
        self.vocabulary_sizes = []
        
        # Resources folder to save the plots
        self.RESOURCES_FOLDER = '../docs/practice-2/resources/'
        self.calculate_statistics()
        
    def calculate_statistics(self):
        """
        Calculates statistics for the collection.
        """
        self.collection_size = len(self.collection.parsed_documents)
        
        for doc in self.collection.parsed_documents:
            content = list(doc.values())[0]
            tokens = self.collection.text_processor.pre_processing(content)
            
            doc_length = len(tokens)  # Calculate document length
            self.document_lengths.append(doc_length)
            
            term_length = len(set(tokens))
            self.term_lengths.append(term_length)
            
            self.vocabulary_sizes.append(len(self.collection.inverted_index))
            
    def display_statistics(self):
        """
        Displays statistics for the collection.
        """
        print('Collection Size:', self.collection_size)
        print('Average Document Length:', sum(self.document_lengths) / self.collection_size)
        print('Average Term Length:', sum(self.term_lengths) / self.collection_size)
        print('Average Vocabulary Size:', sum(self.vocabulary_sizes) / self.collection_size)
        print('Maximum Document Length:', max(self.document_lengths))
        print('Maximum Term Length:', max(self.term_lengths))
        print('Maximum Vocabulary Size:', max(self.vocabulary_sizes))
        print('Minimum Document Length:', min(self.document_lengths))
        print('Minimum Term Length:', min(self.term_lengths))
        print('Minimum Vocabulary Size:', min(self.vocabulary_sizes))
        print('Standard Deviation of Document Lengths:', statistics.stdev(self.document_lengths))
        print('Standard Deviation of Term Lengths:', statistics.stdev(self.term_lengths))
        print('Standard Deviation of Vocabulary Sizes:', statistics.stdev(self.vocabulary_sizes))
        print('Vocabulary Size:', len(self.collection.inverted_index))
        print('Number of Documents:', len(self.collection.parsed_documents))
        print('Number of Terms:', sum(self.term_lengths))
        print('Number of Tokens:', sum(self.document_lengths))
        print('Number of Unique Terms:', len(self.collection.inverted_index))
        print('Number of Unique Tokens:', sum(self.term_lengths))
        
        
    def plot_statistics(self):
        """
        Plot the collection statistics and annotate the plot with additional information.
        """
        plt.figure(figsize=(12, 6))

        # Plot Document Lengths
        plt.subplot(2, 2, 1)
        plt.hist(self.document_lengths, bins=20, edgecolor='k')
        plt.xlabel('Document Length')
        plt.ylabel('Frequency')
        plt.title('Document Length Distribution')
        self.annotate_statistics(plt.gca(), self.document_lengths)

        # Plot Term Lengths
        plt.subplot(2, 2, 2)
        plt.hist(self.term_lengths, bins=20, edgecolor='k')
        plt.xlabel('Term Length')
        plt.ylabel('Frequency')
        plt.title('Term Length Distribution')
        self.annotate_statistics(plt.gca(), self.term_lengths)

        # Plot Vocabulary Sizes
        plt.subplot(2, 2, 3)
        plt.hist(self.vocabulary_sizes, bins=20, edgecolor='k')
        plt.xlabel('Vocabulary Size')
        plt.ylabel('Frequency')
        plt.title('Vocabulary Size Distribution')
        self.annotate_statistics(plt.gca(), self.vocabulary_sizes)

        # Plot Document Length vs Term Length
        plt.subplot(2, 2, 4)
        plt.scatter(self.document_lengths, self.term_lengths, alpha=0.5)
        plt.xlabel('Document Length')
        plt.ylabel('Term Length')
        plt.title('Document Length vs Term Length')
        self.annotate_statistics(plt.gca(), self.document_lengths, x_text='upper right')
        self.annotate_statistics(plt.gca(), self.term_lengths, x_text='upper left')

        plt.tight_layout()
        filename = self.collection.filename.split('/')[-1].split('.')[0]
        plt.savefig(self.RESOURCES_FOLDER + filename + '_statistics.png')
        plt.show()

    def annotate_statistics(self, ax, data, x_text='upper left'):
        """
        Annotate the plot with statistics information.
        """
        ax.text(
            0.05,
            0.95,
            f'Mean: {statistics.mean(data):.2f}',
            verticalalignment='top',
            horizontalalignment=x_text,
            transform=ax.transAxes,
            color='blue',
            fontsize=10,
        )
        ax.text(
            0.05,
            0.90,
            f'Stdev: {statistics.stdev(data):.2f}',
            verticalalignment='top',
            horizontalalignment=x_text,
            transform=ax.transAxes,
            color='red',
            fontsize=10,
        )       