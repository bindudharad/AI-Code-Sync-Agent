"""
Markdown Utilities
"""

import re


class Markdown:

    @staticmethod
    def remove_code_blocks(text):

        return re.sub(
            r"```.*?```",
            "",
            text,
            flags=re.DOTALL
        )

    @staticmethod
    def headings(text):

        return re.findall(
            r"^#+ (.*)",
            text,
            re.MULTILINE
        )

    @staticmethod
    def links(text):

        return re.findall(
            r"\[(.*?)\]\((.*?)\)",
            text
        )

    @staticmethod
    def code_blocks(text):

        return re.findall(
            r"```(.*?)```",
            text,
            re.DOTALL
        )