from enum import Enum
from AIProviders.OpenAIProvider import OpenAIClient
from AIProviders.GeminiProvider import GeminiClient
from lib.functions import get_functions_declarations

from AIProviders.interfaces.AIAssistantProvider import AIAssistantProvider

class AIProviderType(Enum):
    OPENAI = "openai"
    GEMINI = "gemini"

class AIAssistant:
    def __init__(self, default_provider_type: AIProviderType = AIProviderType.OPENAI):

        self.functions_declarations = get_functions_declarations()
        self._providerType = default_provider_type
        self._providers = {
            AIProviderType.OPENAI: OpenAIClient(),
            AIProviderType.GEMINI: GeminiClient(functions=self.functions_declarations),
        }

    def set_provider(self, provider_type: AIProviderType):
        "Alterna o provedor ativo"
        self._providerType = provider_type
        print(f"Provedor alterado para {self._providerType}")

    def generate_response(self, prompt: str) -> str:
        "Delega a chamada para o provedor ativo"
        provider = self._providers.get(self._providerType)
        if not provider:
            raise ValueError("Provedor não configurado")
        return provider.generate_response(prompt)
