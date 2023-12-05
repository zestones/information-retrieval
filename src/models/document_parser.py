import zipfile
import io
import re
import xml.etree.ElementTree as ET
import html
import ftfy


class DocumentParser:
    def __init__(self, filename: str, text_processor, parser_granularity: list):
        self.filename = filename
        self.text_processor = text_processor

        if (parser_granularity is None):
            self.parser_granularity = ['.//article']
        else :
            self.parser_granularity = parser_granularity
        
        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = {}

    def parse_documents(self) -> None:
        """
        Pre-processes the documents.
        """
        parsed_documents = self._parse_documents()
        
        for doc in parsed_documents:
            docno = list(doc.keys())[0]
            content = doc[docno]['terms']
            xpath = doc[docno]['XPath']

            tokens = self.text_processor.pre_processing(content)
            self.parsed_documents[docno] = {'XPath': xpath, 'terms': tokens}
            
    def _parse_documents(self) -> list:
        """
        Parses the document and save the result in a list.
        """
        parsed_documents = []
        if self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for filename in zip_file.namelist():
                    with zip_file.open(filename) as binary_file:
                        with io.TextIOWrapper(binary_file, encoding='utf-8') as f:
                            parsed_documents.extend(
                                self._parse_document_lines(filename, f.readlines()))
        else:
            # open xml file and parse it
            with open(self.filename, 'r') as file:
                parsed_documents.extend(
                    self._parse_document_lines(self.filename, file.readlines()))

        return parsed_documents

    def _parse_document_lines(self, filename: str, lines: list) -> list:
        """
        Parses the document lines and returns a list of dictionaries.
        """
        return self.parse_xml_to_json(filename, lines)
    
    def basic_clean(self, text: str):
        text = ftfy.fix_text(text)
        text = html.unescape(html.unescape(text))
        return text.strip()
    
    def get_xpath(self, element, parent_map):
        path = []
        while element is not None:
            index = 1
            siblings = parent_map.get(element)
            if siblings is not None:
                for sibling in siblings:
                    if sibling is element:
                        break
                    if sibling.tag == element.tag:
                        index += 1
            path.insert(0, f"{element.tag}[{index}]")
            element = parent_map.get(element)
        return '/' + '/'.join(path)

    def extract_text(self, element):
        clean_text = re.sub(r'<[^>]+>', '', ET.tostring(element, encoding='unicode'))
        return clean_text

    def parse_xml_to_json(self, filename: str, lines: list) -> list:
        docno = filename.split('/')[-1].split('.')[0]
        content = ' '.join(lines)

        # TOFIX: can't remove &nbsp; with this regex (replace with a space ?)
        content = re.sub('&[^;]+;', ' ', content)
        
        # Parse XML after handling entities
        root = ET.ElementTree(ET.fromstring(content))
        # Create a dictionary to map child elements to their parents
        parent_map = {c: p for p in root.iter() for c in p}
    
        parsed_documents = []
        root_tag_text = self.extract_text(root.getroot())  # Extract text from the root tag
        if root_tag_text is not None and './/article' in self.parser_granularity:
            root_tag_text = self.basic_clean(root_tag_text)
            xpath = self.get_xpath(root.getroot(), parent_map)
            parsed_documents.append({docno: {'XPath': xpath, 'terms': root_tag_text}})
        
        # Loop through other granularities/tags
        for granularity in self.parser_granularity:
            if granularity == root.getroot().tag:  # Skip the root tag (already processed)
                continue
            
            for balise in root.findall(granularity):
                text = self.extract_text(balise)
                if text is not None:
                    text = self.basic_clean(text)
                    xpath = self.get_xpath(balise, parent_map)  # Get XPath of the element
                    parsed_documents.append({docno: {'XPath': xpath, 'terms': text}})

        return parsed_documents
