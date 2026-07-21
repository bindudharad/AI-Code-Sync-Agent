from ai.base_provider import BaseProvider


class GeminiProvider(BaseProvider):

    def name(self):
        return "Gemini"

    def generate(self, prompt):

        raise NotImplementedError(
            "Connect this class to the Gemini API."
        )