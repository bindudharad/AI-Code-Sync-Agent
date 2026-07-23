
"""
extractor/markdown_parser.py

Extract file paths and fenced code blocks from Markdown produced by
AI assistants (ChatGPT, Kimi, Claude, Gemini, etc.).
"""

import re


class MarkdownParser:
    FILE_PATTERN = re.compile(
        r'^\s*([A-Za-z0-9_\-./\\]+\.[A-Za-z0-9]+)\s*$',
        re.MULTILINE,
    )

    CODE_PATTERN = re.compile(
        r"```([A-Za-z0-9_+-]*)\n(.*?)```",
        re.DOTALL,
    )

    def parse(self, text: str):
        if not text:
            return []

        files = []
        matches = list(self.CODE_PATTERN.finditer(text))

        for match in matches:
            language = (match.group(1) or "").strip()
            code = match.group(2).rstrip()

            prefix = text[:match.start()]
            path = self._find_previous_path(prefix)

            if not path:
                path = f"unknown_file_{len(files)+1}.txt"

            files.append(
                {
                    "path": path,
                    "code": code,
                    "language": language,
                }
            )

        return files

    def _find_previous_path(self, text: str):
        candidates = self.FILE_PATTERN.findall(text)
        if candidates:
            return candidates[-1].replace("\\", "/")
        return ""


if __name__ == "__main__":
    sample = """
backend/app.py

```python
print("Hello")
```

frontend/src/App.tsx

```tsx
export default function App() {
    return <h1>Hello</h1>;
}
```
"""

    parser = MarkdownParser()
    files = parser.parse(sample)

    for f in files:
        print("-" * 40)
        print("Path:", f["path"])
        print("Language:", f["language"])
        print(f["code"])
