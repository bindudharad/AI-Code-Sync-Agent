from bs4 import BeautifulSoup


class DOMReader:

    def __init__(self, page):

        self.page = page

    def html(self):

        return self.page.content()

    def soup(self):

        return BeautifulSoup(
            self.html(),
            "html.parser"
        )

    def text(self):

        return self.soup().get_text()