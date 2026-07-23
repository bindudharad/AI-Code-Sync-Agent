import re


class CodeExtractor:

    CODE_PATTERN = re.compile(
        r"```[a-zA-Z0-9]*\n(.*?)```",
        re.DOTALL
    )

    def extract(self, text):

        codes = []

        for match in self.CODE_PATTERN.finditer(text):
            codes.append(match.group(1))

        return codes