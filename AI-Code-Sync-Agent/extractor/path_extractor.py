import re


class PathExtractor:

    FILE_PATTERN = re.compile(
        r'(?m)^\s*([A-Za-z0-9_\-./\\]+\.[A-Za-z0-9]+)\s*$'
    )

    def extract(self, text: str):

        paths = []

        for match in self.FILE_PATTERN.finditer(text):
            paths.append(match.group(1).strip())

        return paths