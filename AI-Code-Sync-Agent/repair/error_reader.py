from pathlib import Path


class ErrorReader:

    def __init__(self, logfile=None):
        self.logfile = logfile

    def from_file(self):

        if self.logfile is None:
            return ""

        file = Path(self.logfile)

        if not file.exists():
            return ""

        return file.read_text(
            encoding="utf-8",
            errors="ignore"
        )

    def from_result(self, result):

        text = ""

        if "stdout" in result:
            text += result["stdout"]

        if "stderr" in result:
            text += "\n" + result["stderr"]

        return text