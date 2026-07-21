from sync.change_detector import ChangeDetector


class UpdateChecker:

    def __init__(self):

        self.detector = ChangeDetector()

    def needs_update(self, filepath, code):

        return self.detector.changed(
            filepath,
            code
        )