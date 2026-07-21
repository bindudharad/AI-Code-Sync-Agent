from writer.file_writer import FileWriter
from sync.update_checker import UpdateChecker
from sync.history import History


class SyncEngine:

    def __init__(self):

        self.writer = FileWriter()

        self.history = History()

        self.checker = UpdateChecker()

    def sync(self, files):

        created = 0
        updated = 0
        skipped = 0

        for file in files:

            path = file["path"]

            code = file["code"]

            if self.checker.needs_update(
                path,
                code
            ):

                self.writer.write(
                    path,
                    code
                )

                self.history.add(path)

                updated += 1

            else:

                skipped += 1

        print()

        print("=" * 60)

        print("SYNC COMPLETE")

        print("=" * 60)

        print(f"Updated : {updated}")

        print(f"Skipped : {skipped}")

        print(f"Total   : {len(files)}")