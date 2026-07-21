"""
Code Parser
"""

from extractor.html_parser import HTMLParser
from extractor.markdown_parser import MarkdownParser
from extractor.validator import Validator


class CodeParser:
    def __init__(self):
        self.html = HTMLParser()
        self.markdown = MarkdownParser()
        self.validator = Validator()

    def extract(self, text):
        """
        Extract valid files from HTML or Markdown text.

        If the input looks like HTML, convert it to Markdown first.
        Otherwise, parse it directly as Markdown.
        """

        if "<html" in text.lower() or "<body" in text.lower() or "<div" in text.lower():
            text = self.html.parse(text)

        files = self.markdown.parse(text)

        results = []

        for file in files:
            if not self.validator.valid_path(file["path"]):
                continue

            if not self.validator.valid_code(file["code"]):
                continue

            results.append(file)

        return results