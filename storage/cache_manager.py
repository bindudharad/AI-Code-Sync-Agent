import json
from pathlib import Path


class CacheManager:

    CACHE = Path(
        "storage/cache/page_cache.json"
    )

    def save(self, data):

        self.CACHE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.CACHE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4
            )

    def load(self):

        if not self.CACHE.exists():

            return {}

        with open(
            self.CACHE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)