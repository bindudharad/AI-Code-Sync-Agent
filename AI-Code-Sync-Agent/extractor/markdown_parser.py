from extractor.path_extractor import PathExtractor
from extractor.code_extractor import CodeExtractor


class MarkdownParser:

    def __init__(self):

        self.path = PathExtractor()
        self.code = CodeExtractor()

    def parse(self, markdown):

        paths = self.path.extract(markdown)

        codes = self.code.extract(markdown)

        files = []

        for p, c in zip(paths, codes):

            files.append({
                "path": p,
                "code": c
            })

        return files