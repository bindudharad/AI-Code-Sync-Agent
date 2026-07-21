from ai.base_provider import BaseProvider


class CopilotProvider(BaseProvider):

    def name(self):
        return "GitHub Copilot"

    def generate(self, prompt):

        raise NotImplementedError(
            "GitHub Copilot does not expose a general public chat API."
        )