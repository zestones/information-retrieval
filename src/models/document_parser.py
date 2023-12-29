from collections import defaultdict
import xml.etree.ElementTree as ET
import zipfile
import json
import io
import re
from models.xml_parser.xml_parser import XmlParser


class DocumentParser (XmlParser):
    def parse_query_vocabulary(self):
        with open(self.QUERY_FILE, 'r') as file:
            for line in file.readlines():
                query = self.text_processor.pre_processing(line)
                self.query_vocabulary.update(query)

    def parse_documents(self) -> None:

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

    def parse_article(self, tree, docno, parent_map):
        root_tag_text = self.extract_text(tree.getroot())
        if root_tag_text is not None and (self.ARTICLE in self.parser_granularity or self.is_bm25fr):
            self.process_and_update(tree.getroot(), docno, parent_map, root_tag_text)

    def process_and_update(self, element, docno, parent_map, text):
        text = self.clean_and_unescape_text(text)
        xpath = self.get_xpath(element, parent_map)
        tokens = self.text_processor.pre_processing(text)

        tag = re.sub(r'\[\d+\]', '', xpath).split("/")[-1]
        # ! If you want to use a df with a cibled xpath, pass the xpath as tag
        self.update_parsed_documents(docno, tag, tokens)

        # TODO : find a better way to do this
        if self.is_bm25fr and tag == self.ARTICLE[3:]:
            return

        self.update_inverted_index(tokens, docno, xpath)

    def parse_xml_to_json(self, filename: str, lines: list) -> None:
        docno = filename.split('/')[-1].split('.')[0]
        content = ' '.join(lines)
        content = re.sub('&[^;]+;', ' ', content)

        tree = ET.ElementTree(ET.fromstring(content))
        parent_map = self.parent_map(tree)

        self.parse_article(tree, docno, parent_map)

        for parser_granularity in self.parser_granularity:
            if parser_granularity == self.ARTICLE:
                continue
            for balise in tree.findall(parser_granularity):
                self.process_tag(balise, docno, parent_map)

    def process_tag(self, balise, docno, parent_map):
        text = self.extract_text(balise)
        if text is not None:
            self.process_and_update(balise, docno, parent_map, text)

    def update_parsed_documents(self, docno, parser_granularity, tokens):
        if docno not in self.parsed_documents:
            self.parsed_documents[docno] = {parser_granularity: {'terms': tokens, 'N': 1}}
        else:
            if parser_granularity not in self.parsed_documents[docno]:
                self.parsed_documents[docno][parser_granularity] = {'terms': tokens, 'N': 1}
            else:
                self.parsed_documents[docno][parser_granularity]['N'] += 1
                self.parsed_documents[docno][parser_granularity]['terms'].extend(tokens)

    def update_term_frequencies(self, term, docno, granularity):
        self.term_frequencies.setdefault(term, defaultdict(lambda: defaultdict(int)))[granularity][docno] += 1

    def update_inverted_index(self, tokens, docno, xpath):
        for term in tokens:
            if term in self.query_vocabulary:
                if term in self.inverted_index:
                    entries = self.inverted_index[term]
                    if xpath in entries:
                        if docno not in entries[xpath]:
                            entries[xpath].append(docno)
                    else:
                        entries[xpath] = [docno]
                else:
                    self.inverted_index[term] = {xpath: [docno]}

            self.update_term_frequencies(term, docno, xpath)
