from ai.base_provider import BaseProvider


class ClaudeProvider(BaseProvider):

    def name(self):
        return "Claude"

    def generate(self, prompt):

        raise NotImplementedError(
            "Connect this class to Anthropic's Messages API."
        )