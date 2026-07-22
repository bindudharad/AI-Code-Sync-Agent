from bs4 import BeautifulSoup
import re


class KimiReader:

    def __init__(self, browser):
        self.browser = browser

    def get_code_blocks(self):

        page = self.browser.page

        # Wait until page finishes rendering
        page.wait_for_timeout(5000)

        # Scroll to bottom several times
        for _ in range(15):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(300)

        html = page.content()

        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text("\n")

        # Find ### filename followed by ```code```
        pattern = re.compile(
            r"###\s*([^\n]+?)\s*```[a-zA-Z0-9]*\n(.*?)```",
            re.DOTALL,
        )

        files = []

        for match in pattern.finditer(text):

            path = match.group(1).strip()
            code = match.group(2).rstrip()

            files.append(
                {
                    "path": path,
                    "code": code,
                }
            )

        # Debug
        print("=" * 60)
        print("FILES FOUND:", len(files))
        print("=" * 60)

        for f in files[:10]:
            print(f["path"])

        return files