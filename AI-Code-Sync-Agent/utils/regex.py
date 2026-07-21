"""
Regex Utilities
"""

import re


class Regex:

    @staticmethod
    def search(pattern, text):

        return re.search(
            pattern,
            text,
            re.MULTILINE
        )

    @staticmethod
    def find(pattern, text):

        return re.findall(
            pattern,
            text,
            re.MULTILINE
        )

    @staticmethod
    def replace(pattern, repl, text):

        return re.sub(
            pattern,
            repl,
            text
        )

    @staticmethod
    def contains(pattern, text):

        return re.search(
            pattern,
            text
        ) is not None