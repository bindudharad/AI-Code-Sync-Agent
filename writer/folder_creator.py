from pathlib import Path


class FolderCreator:

    @staticmethod
    def create(path: str):

        folder = Path(path).parent

        folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return folder