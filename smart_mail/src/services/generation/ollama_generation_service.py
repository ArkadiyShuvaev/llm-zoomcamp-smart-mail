from typing import Any, Dict
import requests
import json

from common.settings import Settings
from services.generation.generation_result import GenerationResult
from services.generation.generation_service import GenerationService


class OllamaGenerationService(GenerationService):
    """
    OllamaGenerationService is a concrete implementation of the GenerationService
    abstract base class. It uses a local LLM (Language Model) to generate text responses
    based on a given prompt.

    Attributes:
        _settings (Settings): The settings object containing configuration for the local LLM.

    Methods:
        get_answer(prompt: str) -> GenerationResult:
            Generates a text response based on the given prompt using the local LLM.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_answer(self, prompt: str) -> GenerationResult:

        data: Dict[str, Any] = {
            "model": self._settings.local_llm_model_name,
            "prompt": prompt
        }

        response = requests.post(self._settings.local_llm_url, json=data, stream=True)

        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")

        result = ""
        prompt_eval_count = 0
        eval_count = 0

        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                response_data = json.loads(decoded_line)

                if 'response' in response_data:
                    result += response_data['response']

                if 'prompt_eval_count' in response_data:
                    prompt_eval_count = response_data['prompt_eval_count']

                if 'eval_count' in response_data:
                    eval_count = response_data['eval_count']

        generation_result = GenerationResult(
            input_text_token_count=prompt_eval_count,
            token_count=eval_count,
            completion_reason="",
            output_text=result.strip(),
            text_generation_config={},
        )
        return generation_result
