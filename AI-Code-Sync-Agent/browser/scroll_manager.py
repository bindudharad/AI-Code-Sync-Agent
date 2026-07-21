import time


class ScrollManager:

    def __init__(self, page):

        self.page = page

    def scroll_bottom(self):

        self.page.evaluate(
            """
            window.scrollTo(
                0,
                document.body.scrollHeight
            );
            """
        )

    def scroll_top(self):

        self.page.evaluate(
            """
            window.scrollTo(
                0,
                0
            );
            """
        )

    def auto_scroll(self, times=20):

        last_height = 0

        for _ in range(times):

            self.scroll_bottom()

            time.sleep(2)

            new_height = self.page.evaluate(
                "document.body.scrollHeight"
            )

            if new_height == last_height:
                break

            last_height = new_height