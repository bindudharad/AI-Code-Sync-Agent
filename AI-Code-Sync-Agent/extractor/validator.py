from pathlib import Path


class Validator:

    INVALID = [
        "..",
        "<",
        ">",
        "|",
        "?",
        "*",
        '"'
    ]

    def valid_path(self, path):

        if not path:
            return False

        for char in self.INVALID:
            if char in path:
                return False

        return True

    def valid_code(self, code):

        return len(code.strip()) > 0