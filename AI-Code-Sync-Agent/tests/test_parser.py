from extractor.parser import CodeParser


def test_parser():
    parser = CodeParser()

    sample = """
backend/app.py

```python
print("Hello World")

frontend/src/App.tsx

export default function App() {
    return <h1>Hello</h1>;
}

"""

files = parser.extract(sample)

print("Files Found:", len(files))

for file in files:
    print("-" * 40)
    print("Path :", file["path"])
    print("Code :")
    print(file["code"])

if __name__ == "main":
    test_parser()
