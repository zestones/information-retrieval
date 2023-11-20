import zipfile
import io
import re


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
        print("Parsing documents...")
        if self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for filename in zip_file.namelist():
                    with zip_file.open(filename) as binary_file:
                        with io.TextIOWrapper(binary_file, encoding='utf-8') as f:
                            parsed_documents.extend(
                                self._parse_document_lines(filename, f.readlines()))
        else:
            with open(self.filename, 'r', encoding='utf-8') as f:
                parsed_documents = self._parse_document_lines(self.filename, f.readlines())

        return parsed_documents

    def _parse_document_lines(self, filename, lines: list) -> list:
        """
        Parses the document lines and returns a list of dictionaries.
        """
        parsed_documents = []
        docno = filename.split('/')[-1].split('.')[0]

        content = ' '.join(lines)

        # remove the xml tags with a regex
        content = re.sub('<[^<]+>', '', content)

        # remove the newlines
        content = content.replace('\n', ' ')

        # remove the multiple spaces
        content = re.sub(' +', ' ', content)

        # remove the leading and trailing spaces
        content = content.strip()

        parsed_documents.append({docno: content})

        return parsed_documents
