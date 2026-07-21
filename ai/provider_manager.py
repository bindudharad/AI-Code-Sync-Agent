from ai.chatgpt import ChatGPTProvider
from ai.kimi import KimiProvider
from ai.claude import ClaudeProvider
from ai.gemini import GeminiProvider
from ai.deepseek import DeepSeekProvider
from ai.copilot import CopilotProvider


class ProviderManager:

    def __init__(self):

        self.providers = {
            "chatgpt": ChatGPTProvider(),
            "kimi": KimiProvider(),
            "claude": ClaudeProvider(),
            "gemini": GeminiProvider(),
            "deepseek": DeepSeekProvider(),
            "copilot": CopilotProvider()
        }

    def get(self, provider):

        return self.providers.get(provider.lower())