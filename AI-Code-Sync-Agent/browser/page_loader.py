import time


class PageLoader:

    def __init__(self, page):

        self.page = page

    def open(self, url):

        self.page.goto(
            url,
            wait_until="networkidle"
        )

    def wait(self, seconds):

        time.sleep(seconds)

    def title(self):

        return self.page.title()

    def html(self):

        return self.page.content()