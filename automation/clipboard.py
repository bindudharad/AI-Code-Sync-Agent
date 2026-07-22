import pyperclip
import time


class ClipboardWatcher:

    def __init__(self):

        self.previous = ""

    def listen(self, callback):

        while True:

            current = pyperclip.paste()

            if current != self.previous:

                self.previous = current

                callback(current)

            time.sleep(1)