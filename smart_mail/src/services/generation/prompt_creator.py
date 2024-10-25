import os
from typing import List
from jinja2 import Environment, FileSystemLoader, PackageLoader

from services.generation.generation_result import GenerationResult
from services.search_result import SearchResult

class PromptCreator:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        template_dir = os.path.join(base_dir, "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        self._template = env.get_template('prompt_template.jinja2')

    def create(self, question: str, documents: List[SearchResult]) -> str:
        """
        Create a prompt for answering a customer's question.

        Args:
            question (str): The customer's question.
            documents (List[SearchResult]): The search results from the internal database.

        Returns:
            str: The generated prompt.
        """

        # TODO: Add condition to analyze the project name if one exists in the search results.
        result = self._template.render(
            # general_instructions=general_instructions,
            # model_instructions=model_instructions,
            question=question,
            documents=List[SearchResult]
        )

        return result
