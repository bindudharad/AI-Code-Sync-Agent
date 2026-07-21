import time


class Retry:

    def __init__(self, retries=3, delay=2):

        self.retries = retries

        self.delay = delay

    def execute(self, func, *args, **kwargs):

        last = None

        for attempt in range(self.retries):

            try:

                return func(*args, **kwargs)

            except Exception as e:

                last = e

                print(
                    f"Retry {attempt+1}/{self.retries}"
                )

                time.sleep(self.delay)

        raise last