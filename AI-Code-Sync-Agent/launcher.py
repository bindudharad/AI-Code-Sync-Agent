from browser.chrome import ChromeController
from extractor.parser import CodeParser
from writer.file_writer import FileWriter


class Launcher:

    def __init__(self):
        self.browser = ChromeController()
        self.parser = CodeParser()
        self.writer = FileWriter()

    def start(self):

        print("=" * 60)
        print("AI CODE SYNC AGENT")
        print("=" * 60)

        print("[1] Opening Browser...")
        html = self.browser.get_page_source()

        print("[2] Extracting Files...")
        files = self.parser.extract(html)

        print(f"Found {len(files)} files")

        print("[3] Writing Files...")

        for file in files:
            self.writer.write(
                file["path"],
                file["code"]
            )

        print("\nDone!")