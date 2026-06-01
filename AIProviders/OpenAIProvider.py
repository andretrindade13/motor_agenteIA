import os
from openai import OpenAI, APIError
from AIProviders.interfaces.AIAssistantProvider import AIAssistantProvider

class AIProviderError(Exception):
    """Exceção genérica para erros de provedor de IA."""
    pass

class OpenAIClient(AIAssistantProvider):
    def __init__(self, model: str = "gpt-5.4-mini"):
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        self.model = model

        if not api_key:
            raise AIProviderError("OPENAI_API_KEY não foi definida.")

        self.client = OpenAI(api_key=api_key)
    def generate_response(self, prompt: str) -> str | None:
        try:
            response = self.client.responses.create(
                model=self.model,
                input=prompt
            )

            return response.output_text

        except APIError as e:
            print(f"Erro na API do OpenAI: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")