from ai.base_provider import BaseProvider


class DeepSeekProvider(BaseProvider):

    def name(self):
        return "DeepSeek"

    def generate(self, prompt):

        raise NotImplementedError(
            "Connect this class to the DeepSeek API."
        )