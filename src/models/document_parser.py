from collections import defaultdict
import xml.etree.ElementTree as ET
import zipfile
import time
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
        self.parsed_documents_time_processing = 0
        self.inverted_index_time_processing = 0
        self.extract_text_time_processing = 0
        self.xml_to_json_time_processing = 0
        self.xpath_time_processing = 0
        self.clean_time_processing = 0
        self.tf_time_processing = 0

        self.parse_query_vocabulary()
        if self.filename.endswith('.zip'):
            with zipfile.ZipFile(self.filename, 'r') as zip_file:
                for file in zip_file.namelist():
                    with zip_file.open(file) as xml_file:
                        self.parse_xml_to_json(file, xml_file)
        elif self.filename.endswith('.xml'):
            with open(self.filename, 'rb') as xml_file:
                self.parse_xml_to_json(self.filename, xml_file)

        self.inverted_index_time_processing -= self.tf_time_processing
    
    def parse_article(self, tree, docno, parent_map):
        start = time.time()
        root_tag_text = self.extract_text(tree.getroot())
        end = time.time()
        self.extract_text_time_processing += end - start

        if root_tag_text is not None and (self.ARTICLE in self.parser_granularity or self.is_bm25fr):
            self.process_and_update(tree.getroot(), docno, parent_map, root_tag_text)

    def process_and_update(self, element, docno, parent_map, text):
        start = time.time()
        xpath = self.get_xpath(element, parent_map)
        end = time.time()
        self.xpath_time_processing += end - start

        start = time.time()
        tokens = text.split()
        end = time.time()
        self.clean_time_processing += end - start

        tag = re.sub(r'\[\d+\]', '', xpath).split("/")[-1]
        # ! If you want to use a df with a cibled xpath, pass the xpath as tag
        self.update_parsed_documents(docno, tag, tokens)

        if self.is_bm25fr and tag == self.ARTICLE[3:]:
            return

        self.update_inverted_index(tokens, docno, xpath)

    def parse_xml_to_json(self, filename: str, xml_file: io.TextIOWrapper) -> None:
        start = time.time()
        docno = filename.split('/')[-1].split('.')[0]
        
        xml_content = xml_file.read().decode('utf-8')
        tree = ET.ElementTree(ET.fromstring(re.sub('&[^;]+;', ' ', xml_content)))

        parent_map = self.parent_map(tree)
        self.parse_article(tree, docno, parent_map)

        for parser_granularity in self.parser_granularity:
            if parser_granularity == self.ARTICLE:
                continue
            for balise in tree.findall(parser_granularity):
                self.process_tag(balise, docno, parent_map)
        end = time.time()
        self.xml_to_json_time_processing += end - start

    def process_tag(self, balise, docno, parent_map):
        start = time.time()
        text = self.extract_text(balise)
        end = time.time()
        self.extract_text_time_processing += end - start
        if text is not None:
            self.process_and_update(balise, docno, parent_map, text)

    def update_parsed_documents(self, docno, parser_granularity, tokens):
        start = time.time()
        if docno not in self.parsed_documents:
            self.parsed_documents[docno] = {parser_granularity: {'terms': tokens, 'N': 1}}
        else:
            if parser_granularity not in self.parsed_documents[docno]:
                self.parsed_documents[docno][parser_granularity] = {'terms': tokens, 'N': 1}
            else:
                self.parsed_documents[docno][parser_granularity]['N'] += 1
                self.parsed_documents[docno][parser_granularity]['terms'].extend(tokens)

        end = time.time()
        self.parsed_documents_time_processing += end - start

    def update_term_frequencies(self, term, docno, granularity):
        start_time = time.time()
        self.term_frequencies.setdefault(term, defaultdict(lambda: defaultdict(int)))[granularity][docno] += 1
        end_time = time.time()
        self.tf_time_processing += end_time - start_time

    def update_inverted_index(self, tokens, docno, xpath):
        start_time = time.time()
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

        end_time = time.time()
        self.inverted_index_time_processing += end_time - start_time
