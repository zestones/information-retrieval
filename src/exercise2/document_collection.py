from exercise2.text_processor import TextProcessor
from colorama import Fore, Style


"""
    This class represents a collection of documents.
    The class provides methods to read the documents from a file, 
    construct the inverted index, and calculate term frequencies.
"""
class DocumentCollection:
    def __init__(self, filename) -> None:
        self.filename = filename
        self.text_processor = TextProcessor()
        self.inverted_index = {}

    def read_documents(self) -> list:
        """
        Reads the documents from the file.
        """
        with open(self.filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            result = []
            for line in lines:
                if '<doc><docno>' in line:
                    docno = line.split('<doc><docno>')[1].split('</docno>')[0]
                    content = line.split('</docno>')[1].split('</doc>')[0]
                    result.append({docno: content})

            return result

    def construct_inverted_index(self, collection: list) -> dict:
        """
        Constructs the inverted index.
        """
        index = {}
        term_frequencies = {}

        for doc in collection:
            docno = list(doc.keys())[0]
            content = list(doc.values())[0]

            tokens = self.text_processor.post_processing(content)

            for token in tokens:
                if token not in index:
                    index[token] = [docno]
                    term_frequencies[token] = {docno: 1}
                else:
                    term_frequencies.setdefault(token, {}).setdefault(docno, 0)
                    term_frequencies[token][docno] += 1
                    
                    if docno not in index[token]:
                        index[token].append(docno)

        self.inverted_index = index
        self.term_frequencies = term_frequencies
        return index

    def document_frequency(self, term: str) -> int:
        """
        Returns the document frequency of a term.
        """
        return len(self.inverted_index.get(term, []))
    
    def term_frequency(self, docno: str, term: str) -> int:
        """
        Returns the term frequency of a term in a document.
        """
        return self.term_frequencies.get(term, {}).get(docno, 0)
    
    def print_title(self, text: str) -> None:
        """
        Prints a title.
        """
        print(Fore.BLUE + text + Style.RESET_ALL)
        print('-' * len(text))

    def display_index(self) -> None:
        """
        Displays the inverted index.
        """
        self.print_title('Inverted Index')
        for term, docnos in self.inverted_index.items():
            docno_list = ', '.join([f'{Fore.GREEN}{docno}{Style.RESET_ALL}' for docno in docnos])
            print(f"{term}: {docno_list}")

        print()

    def display_term_frequencies(self) -> None:
        """
        Displays the term frequencies.
        """
        self.print_title('Term Frequencies')
        
        for term in self.term_frequencies:
            print(term, end=': ')
            for docno in self.term_frequencies[term]:
                print(Fore.GREEN + docno + Style.RESET_ALL + '(' + str(self.term_frequencies[term][docno]) + ')', end=' ')
            print()
        
        print()