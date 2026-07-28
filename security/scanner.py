import re


class Scanner:

    PATTERNS = [

        r"rm\s+-rf",

        r"del\s+/f",

        r"shutdown",

        r"format\s+",

        r"os\.system",

        r"subprocess",

        r"eval\(",

        r"exec\("

    ]

    def scan(self, code):

        issues = []

        for pattern in self.PATTERNS:

            if re.search(

                pattern,

                code,

                re.IGNORECASE

            ):

                issues.append(pattern)

        return issues

    def safe(self, code):

        return len(self.scan(code)) == 0