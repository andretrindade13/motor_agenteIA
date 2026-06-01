from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv()

class AIAssistantProvider(ABC):

    @abstractmethod
    def generate_response(self: object, prompt: str) -> str:
        """
            Generate a response
        :return:
        """
        pass