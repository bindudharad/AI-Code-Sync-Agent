from ai.base_provider import BaseProvider


class KimiProvider(BaseProvider):

    def name(self):
        return "Kimi"

    def generate(self, prompt):

        raise NotImplementedError(
            "Connect this class to Kimi's official API if available."
        )