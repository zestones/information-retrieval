import xml.etree.ElementTree as ET
import html
import ftfy
import re


class XmlParser:
    def __init__(self, xml_file):
        """
        Initializes an instance of the XmlParser class.

        Args:
            xml_file (str): The path to the XML file to be parsed.
            granularity (list): A list specifying the granularity of the XML parsing.

        Attributes:
            xml_file (str): The path to the XML file to be parsed.
        """
        self.xml_file = xml_file

    def get_xpath(self, element, parent_map):
        """
        Returns the XPath of the given XML element.

        Args:
            element (xml.etree.ElementTree.Element): The XML element for which to retrieve the XPath.
            parent_map (dict): A dictionary mapping each XML element to its parent element.

        Returns:
            str: The XPath of the given XML element.
        """
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

    def parent_map(self, tree):
        """
        Returns a dictionary mapping each XML element to its parent element.

        Args:
            tree (xml.etree.ElementTree.ElementTree): The XML tree to be parsed.

        Returns:
            dict: A dictionary mapping each XML element to its parent element.
        """
        return {c: p for p in tree.iter() for c in p}

    def clean_and_unescape_text(self, text: str):
        """
        Cleans and unescapes the given text.

        Args:
            text (str): The text to be cleaned and unescaped.

        Returns:
            str: The cleaned and unescaped text.
        """
        return html.unescape(html.unescape(ftfy.fix_text(text))).strip()

    def extract_text(self, element):
        """
        Extracts the text content from an XML element.

        Args:
            element (xml.etree.ElementTree.Element): The XML element from which to extract the text.

        Returns:
            str: The extracted text content.
        """
        clean_text = self.tag_pattern.sub('', ET.tostring(element, encoding='unicode'))
        return clean_text
