from abc import ABC, abstractmethod
from services.generation.generation_result import GenerationResult


class GenerationService(ABC):

    @abstractmethod
    def get_answer(self, prompt: str) -> GenerationResult:
        """
        Generates a text response based on the given prompt using an LLM.

        Args:
            prompt (str): The input text prompt for generating the response.

        Returns:
            GenerationResult: The result of the text generation, including token counts and the generated text.
        """
        pass
