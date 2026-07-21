from bs4 import BeautifulSoup


class HTMLParser:

    def parse(self, html):

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        return soup.get_text("\n")