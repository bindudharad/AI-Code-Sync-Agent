"""
extractor/html_parser.py

Improved HTML parser for Kimi / ChatGPT / Claude exported pages.
"""

from html.parser import HTMLParser as BaseHTMLParser
import re


FILE_RE = re.compile(
    r'([A-Za-z0-9_\-./\\]+\.[A-Za-z0-9]+)'
)


class _CodeHTMLParser(BaseHTMLParser):

    def __init__(self):
        super().__init__()

        self.files = []

        self.in_pre = False
        self.buffer = []

        self.last_lines = []

    def handle_starttag(self, tag, attrs):

        if tag == "pre":
            self.in_pre = True
            self.buffer = []

    def handle_endtag(self, tag):

        if tag != "pre":
            return

        self.in_pre = False

        code = "".join(self.buffer).strip()

        if not code:
            return

        path = self.find_path()

        if not path:
            return

        self.files.append(
            {
                "path": path,
                "code": code,
                "language": "",
            }
        )

        self.buffer = []

    def handle_data(self, data):

        if self.in_pre:
            self.buffer.append(data)
            return

        for line in data.splitlines():

            line = line.strip()

            if line:

                self.last_lines.append(line)

                if len(self.last_lines) > 20:
                    self.last_lines.pop(0)

    def find_path(self):

        for line in reversed(self.last_lines):

            m = FILE_RE.search(line)

            if m:

                return m.group(1).replace("\\", "/")

        return ""


class HTMLParser:

    def parse(self, html):

        parser = _CodeHTMLParser()

        parser.feed(html)

        parser.close()

        return parser.files