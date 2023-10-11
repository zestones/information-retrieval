import zipfile
import gzip
import io


class DocumentParser:
    def __init__(self, filename: str, text_processor):
        self.filename = filename
        self.text_processor = text_processor

        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = []

    def parse_documents(self) -> None:
        """
        Pre-processes the documents.
        """
        parsed_documents = self._parse_documents()
        for doc in parsed_documents:
            docno = list(doc.keys())[0]
            content = list(doc.values())[0]

            tokens = self.text_processor.pre_processing(content)
            self.parsed_documents.append({docno: tokens})

    def _parse_documents(self) -> list:
        """
        Parses the document and save the result in a list.
        """
        parsed_documents = []
        if (self.filename.endswith('.gz')):
            with gzip.open(self.filename, 'rt', encoding='utf-8') as f:
                parsed_documents = self._parse_document_lines(f.readlines())
        elif self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                parsed_documents = []
                for file_name in zip_file.namelist():
                    with zip_file.open(file_name) as binary_file:
                        with io.TextIOWrapper(binary_file, encoding='utf-8') as f:
                            parsed_documents.extend(self._parse_document_lines(f.readlines()))
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                parsed_documents = self._parse_document_lines(f.readlines())

        return parsed_documents

    def _parse_document_lines(self, lines: str) -> list:
        """
        Parses the document lines and returns a list of dictionaries.
        """
        parsed_dictionary = []
        current_content = ''

        for line in lines:
            if '<doc><docno>' in line:
                docno = line.split('<doc><docno>')[1].split('</docno>')[0]
            elif '</doc>' in line:
                parsed_dictionary.append({docno: current_content})
                current_content = ''
            else:
                current_content += line

        return parsed_dictionary
