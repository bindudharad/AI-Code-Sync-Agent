import re


class LogParser:

    PATTERNS = {

        "module_not_found":
            r"Module not found",

        "syntax_error":
            r"SyntaxError",

        "import_error":
            r"ImportError",

        "type_error":
            r"TypeError",

        "reference_error":
            r"ReferenceError",

        "file_not_found":
            r"No such file",

        "permission":
            r"Permission denied"

    }

    def parse(self, log):

        issues = []

        for name, pattern in self.PATTERNS.items():

            if re.search(pattern, log, re.IGNORECASE):

                issues.append(name)

        return issues