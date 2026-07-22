import threading
import time


class Scheduler:

    def every(self, seconds, func, *args, **kwargs):

        def runner():

            while True:

                func(*args, **kwargs)

                time.sleep(seconds)

        thread = threading.Thread(
            target=runner,
            daemon=True
        )

        thread.start()

        return thread