from pathlib import Path
import hashlib


class ChangeDetector:

    def checksum(self, text):

        return hashlib.sha256(

            text.encode("utf-8")

        ).hexdigest()

    def changed(self, filepath, new_code):

        file = Path(filepath)

        if not file.exists():
            return True

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            old = f.read()

        return self.checksum(old) != self.checksum(new_code)