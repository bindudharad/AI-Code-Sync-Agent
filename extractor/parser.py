
"""
extractor/parser.py

High-level parser that extracts project files from AI responses.
"""

from extractor.markdown_parser import MarkdownParser
from extractor.html_parser import HTMLParser
from extractor.validator import Validator


class CodeParser:
    def __init__(self):
        self.markdown = MarkdownParser()
        self.html = HTMLParser()
        self.validator = Validator()

    def extract(self, text: str):
        """
        Extract files from markdown or HTML.

        Returns:
            [
                {
                    "path": "...",
                    "code": "...",
                    "language": "python"
                }
            ]
        """
        if not text:
            return []

        text = text.strip()

        if "<html" in text.lower() or "<body" in text.lower():
            files = self.html.parse(text)
        else:
            files = self.markdown.parse(text)

        cleaned = []
        seen = set()

        for item in files:
            path = item.get("path", "").strip()
            code = item.get("code", "")
            lang = item.get("language", "")

            if not self.validator.valid_path(path):
                continue

            if not self.validator.valid_code(code):
                continue

            if path in seen:
                continue

            seen.add(path)

            cleaned.append({
                "path": path,
                "code": code.rstrip(),
                "language": lang,
            })

        return cleaned

    def summary(self, files):
        return {
            "total_files": len(files),
            "paths": [f["path"] for f in files],
        }


if __name__ == "__main__":
    sample = r"""
backend/app.py

```python
print("Hello World")
```

frontend/src/App.tsx

```tsx
export default function App() {
    return <h1>Hello</h1>;
}
```
"""

    parser = CodeParser()
    result = parser.extract(sample)

    print(parser.summary(result))

    for f in result:
        print("-" * 40)
        print("PATH :", f["path"])
        print("LANG :", f["language"])
        print(f["code"])
