import time


class LiveSync:

    def __init__(self):

        self.running = False

    def start(self):

        self.running = True

        print("Live Sync Started")

    def stop(self):

        self.running = False

        print("Live Sync Stopped")

    def wait(self, seconds=2):

        time.sleep(seconds)