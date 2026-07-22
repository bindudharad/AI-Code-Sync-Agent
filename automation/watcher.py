from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time


class ChangeHandler(FileSystemEventHandler):

    def __init__(self, callback):

        self.callback = callback

    def on_modified(self, event):

        if not event.is_directory:

            self.callback(event.src_path)


class FolderWatcher:

    def watch(self, folder, callback):

        handler = ChangeHandler(callback)

        observer = Observer()

        observer.schedule(
            handler,
            folder,
            recursive=True
        )

        observer.start()

        print(f"Watching: {folder}")

        try:

            while True:

                time.sleep(1)

        except KeyboardInterrupt:

            observer.stop()

        observer.join()