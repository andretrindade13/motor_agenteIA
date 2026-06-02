import os
from google import genai
from google.genai import types
from google.genai.errors import APIError
from src.tools.AIAssistantProvider import AIAssistantProvider
from src.tools.functions.emails_verify import emails_verify


class AIProviderError(Exception):
    """Exceção genérica para erros de provedor de IA."""
    pass

class GeminiClient(AIAssistantProvider):
    def __init__(self, model: str = "gemini-3.5-flash", functions=None):
        self.functions = functions if functions is not None else []
        self.model = model

        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise AIProviderError("OPENAI_API_KEY não foi definida.")

        self.client = genai.Client(api_key=api_key)
        if self.functions:
            tools = types.Tool(function_declarations=self.functions)
            self.config = types.GenerateContentConfig(tools=[tools])

    def generate_response(self, prompt: str) -> str | None:

        contents = [
            types.Content(
                role="user", parts=[types.Part(text=prompt)]
            )
        ]
        try:
            response = self.client.models.generate_content(
                model= self.model,
                contents= contents,
                config= self.config
            )

            tool_call = response.candidates[0].content.parts[0].function_call
            if tool_call is not None:
                if tool_call.name == "emails_verify":
                    print(tool_call.args)
                    result = emails_verify(**tool_call.args)

                    function_response_part = types.Part.from_function_response(
                        name=tool_call.name,
                        response={"result": result},
                    )

                    contents.append(response.candidates[0].content)  # Append the content from the model's response.
                    contents.append(
                        types.Content(role="user", parts=[function_response_part]))  # Append the function response

                client = genai.Client()
                final_response = client.models.generate_content(
                    model=self.model,
                    config=self.config,
                    contents=contents,
                )
                return final_response.text
            return response.text
        except APIError as e:
            print(f"Erro na API do Gemini: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")