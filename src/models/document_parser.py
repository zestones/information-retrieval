from collections import defaultdict
import xml.etree.ElementTree as ET
import zipfile
import html
import ftfy
import json
import io
import re


class DocumentParser:
    def __init__(self, filename: str, text_processor, parser_granularity: list):
        self.filename = filename
        self.text_processor = text_processor

        self.ARTICLE = './/article'
        self.QUERY_FILE = '../lib/data/practice_04/topics_M2DSC_7Q.txt'

        self.query_vocabulary = set()

        if (parser_granularity is None):
            self.parser_granularity = [self.ARTICLE]
        else:
            self.parser_granularity = parser_granularity

        # A dictionary with the document number as key and the content as value
        # ex: {'doc1': [This, is, the, content, of, the, document]}
        self.parsed_documents = {}
        self.inverted_index = defaultdict(list)
        self.term_frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.already_processed = set()

    def parse_query_vocabulary(self):
        with open(self.QUERY_FILE, 'r') as file:
            for line in file.readlines():
                query = self.text_processor.pre_processing(line)
                self.query_vocabulary.update(query)

    def parse_documents(self) -> None:
        """
        Pre-processes the documents.
        """
        self.parse_query_vocabulary()

        if self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for filename in zip_file.namelist():
                    with zip_file.open(filename) as binary_file:
                        with io.TextIOWrapper(binary_file, encoding='utf-8') as f:
                            self.parse_xml_to_json(filename, f.readlines())
        else:
            with open(self.filename, 'r') as file:
                self.parse_xml_to_json(self.filename, file.readlines())

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

    def parse_xml_to_json(self, filename: str, lines: list) -> None:
        docno = filename.split('/')[-1].split('.')[0]
        content = ' '.join(lines)
        content = re.sub('&[^;]+;', ' ', content)

        root = ET.ElementTree(ET.fromstring(content))
        parent_map = {c: p for p in root.iter() for c in p}

        root_tag_text = self.extract_text(root.getroot())
        if root_tag_text is not None and self.ARTICLE in self.parser_granularity:
            root_tag_text = self.basic_clean(root_tag_text)
            xpath = self.get_xpath(root.getroot(), parent_map)
            tokens = self.text_processor.pre_processing(root_tag_text)
            self.parsed_documents.setdefault(docno, []).append({'XPath': xpath, 'terms': tokens})
            self.update_inverted_index(tokens, docno, xpath, self.ARTICLE)

        for parser_granularity in self.parser_granularity:
            if parser_granularity == self.ARTICLE:
                continue
            for balise in root.findall(parser_granularity):
                text = self.extract_text(balise)
                if text is not None:
                    xpath = self.get_xpath(balise, parent_map)
                    text = self.basic_clean(text)
                    tokens = self.text_processor.pre_processing(text)

                    self.parsed_documents.setdefault(docno, []).append(
                        {'XPath': xpath, 'terms': tokens})
                    self.update_inverted_index(tokens, docno, xpath, parser_granularity)

    def update_term_frequencies(self, term, docno, granularity):
        self.term_frequencies.setdefault(term, defaultdict(lambda: defaultdict(int)))[
            granularity][docno] += 1

    def update_inverted_index(self, tokens, docno, last_xpath, granularity):
        for term in tokens:
            if term in self.query_vocabulary:
                if term in self.inverted_index:
                    entries = self.inverted_index[term]
                    if granularity in entries:
                        entries[granularity][docno] = last_xpath
                    else:
                        entry = {docno: last_xpath}
                        entries[granularity] = entry
                else:
                    entry = {docno: last_xpath}
                    self.inverted_index[term] = {granularity: entry}

            self.update_term_frequencies(term, docno, granularity)
