from ai.base_provider import BaseProvider


class ChatGPTProvider(BaseProvider):

    def name(self):
        return "ChatGPT"

    def generate(self, prompt):

        raise NotImplementedError(
            "Connect this class to the official ChatGPT API."
        )