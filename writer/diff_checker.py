from pathlib import Path
import difflib


class DiffChecker:

    @staticmethod
    def compare(filepath, new_code):

        file = Path(filepath)

        if not file.exists():

            return "NEW FILE"

        old = file.read_text(
            encoding="utf-8"
        )

        diff = difflib.unified_diff(

            old.splitlines(),

            new_code.splitlines(),

            fromfile="Old",

            tofile="New",

            lineterm=""
        )

        return "\n".join(diff)