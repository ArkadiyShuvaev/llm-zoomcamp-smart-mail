import os
from typing import List
from jinja2 import Environment, FileSystemLoader

from data_loaders.repayment_schedule_loader import Repayment
from services.generation.generation_result import GenerationResult
from services.search_result import SearchResult

class PromptCreator:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        print(base_dir)
        template_dir = os.path.join(base_dir, "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        self._template = env.get_template('prompt_template.jinja2')

    def create(self,
               question: str,
               documents: List[SearchResult],
               repayment_schedule: List[Repayment]) -> str:
        """
        Create a prompt for answering a customer's question.

        Args:
            question (str): The customer's question.
            documents (List[SearchResult]): The search results from the internal database.
            repayment_schedule (List[Repayment]): The repayment schedule for the customer's project. Only one project is supported in the current implementation.

        Returns:
            str: The generated prompt.
        """

        customer_context = None
        if len(repayment_schedule) > 0:
            customer_context = {
                "repayment_schedule_items": repayment_schedule
            }

        # TODO: Add condition to analyze the project name if one exists in the search results.
        result = self._template.render(
            question=question,
            documents=documents,
            no_result_answer=GenerationResult.empty().output_text,
            customer_context = customer_context
        )

        return result
