
"""
extractor/detector.py

Detects the format/source of AI responses and selects
the appropriate extraction strategy.
"""

import re


class ResponseDetector:
    MARKDOWN_FENCE = re.compile(r"```[\w+-]*\n", re.MULTILINE)

    def detect(self, content: str) -> dict:
        """
        Returns metadata describing the content.

        Example:
        {
            "type": "markdown",
            "source": "chat",
            "has_code": True
        }
        """
        if not content:
            return {
                "type": "unknown",
                "source": "unknown",
                "has_code": False,
            }

        text = content.strip().lower()

        has_html = "<html" in text or "<body" in text or "<pre" in text
        has_markdown = bool(self.MARKDOWN_FENCE.search(content))
        has_code = has_html or has_markdown

        source = "unknown"

        if "chatgpt" in text:
            source = "chatgpt"
        elif "kimi" in text:
            source = "kimi"
        elif "claude" in text:
            source = "claude"
        elif "gemini" in text:
            source = "gemini"

        if has_html:
            ctype = "html"
        elif has_markdown:
            ctype = "markdown"
        else:
            ctype = "plain"

        return {
            "type": ctype,
            "source": source,
            "has_code": has_code,
        }

    def is_markdown(self, content: str) -> bool:
        return self.detect(content)["type"] == "markdown"

    def is_html(self, content: str) -> bool:
        return self.detect(content)["type"] == "html"

    def has_code_blocks(self, content: str) -> bool:
        return self.detect(content)["has_code"]


if __name__ == "__main__":
    detector = ResponseDetector()

    samples = [
        "backend/app.py\n\n```python\nprint('hi')\n```",
        "<html><body><pre><code>print('hi')</code></pre></body></html>",
        "Just some plain text."
    ]

    for sample in samples:
        print(detector.detect(sample))
