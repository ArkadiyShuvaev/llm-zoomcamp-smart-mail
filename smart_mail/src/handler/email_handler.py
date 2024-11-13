import time
import logging
from typing import Dict, Any, List

from common.settings import Settings
from data_loaders.repayment_schedule_loader import RepaymentScheduleLoader
from services.database.database_service import DatabaseService
from services.generation.generation_result import GenerationResult
from services.generation.generation_service import GenerationService
from services.generation.prompt_creator import PromptCreator
from services.retrieval_service import RetrievalService
from services.reciprocal_rank_fusion_service import ReciprocalRankFusionService
from services.content.content_data_preparer import ContentDataPreparer
from services.search_result import SearchResult
from dtos.identified_project import IdentifiedProject


class EmailHandler:
    """
    Handles incoming emails and performs various operations on them.
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_creator: PromptCreator,
        generation_service: GenerationService,
        database_service: DatabaseService,
        reciprocal_rank_fusion_service: ReciprocalRankFusionService,
        content_data_preparer: ContentDataPreparer,
        settings: Settings
    ) -> None:
        self._retrieval_service = retrieval_service
        self._prompt_creator = prompt_creator
        self._generation_service = generation_service
        self._database_service = database_service
        self.reciprocal_rank_fusion_service = reciprocal_rank_fusion_service
        self._content_data_preparer = content_data_preparer
        self._settings = settings
        self._logger = logging.getLogger(__name__)

    def handle(self, email_from: str, subject: str, body: str) -> str:
        self._logger.info("Handling email from: %s, subject: %s", email_from, subject)

        start_time = time.time()

        question = subject + " " + body
        identified_project = self._content_data_preparer.extract_project(question)
        identified_project_id = str(identified_project.id) if identified_project is not None else None
        user_authorization_ids = self._content_data_preparer.get_user_authorization_ids(email_from)

        self._logger.info("Processing content for the extracted project: %s", identified_project)

        search_params = self._create_search_params(question, identified_project, user_authorization_ids)
        retrieval_result = self._retrieval_service.search(**search_params)

        reranked_search_results = self.reciprocal_rank_fusion_service.rerank(retrieval_result)
        prompt, generation_result, elapsed_llm_time = self._generate_answer(body, reranked_search_results, email_from, identified_project_id)

        end_time = time.time()
        elapsed_time = end_time - start_time

        created_entity = self._save_to_database(email_from, subject, body, prompt, generation_result, elapsed_llm_time, elapsed_time)
        self._logger.info(f"Created entity: {created_entity}")

        return str(generation_result.output_text)

    def _generate_answer(self, question: str, reranked_search_results: List[SearchResult], email_from: str, extracted_project_id: str | None) -> tuple[str, GenerationResult, float]:
        if len(reranked_search_results) == 0:
            return "", GenerationResult.empty(), 0.0

        used_results = reranked_search_results[:10]
        prompt = self._prompt_creator.create(question, used_results, RepaymentScheduleLoader.get_repayment_schedule(email_from, extracted_project_id))

        start_llm_time = time.time()
        # TODO: Add exception handling
        generation_result = self._generation_service.get_answer(prompt)
        end_llm_time = time.time()
        elapsed_llm_time = end_llm_time - start_llm_time
        return prompt, generation_result, elapsed_llm_time

    def _create_search_params(self,
                              question: str,
                              identified_project: IdentifiedProject | None,
                              user_authorization_ids: List[str] | None) -> Dict[str, Any]:
        search_params: Dict[str, Any] = {"question": question}

        if identified_project is not None:
            search_params["customer_project_id"] = str(identified_project.id)

        if user_authorization_ids is not None:
            search_params["authorization_ids"] = user_authorization_ids

        return search_params

    def _save_to_database(self, email_from: str, subject: str, body: str, prompt: str,
                          generation_result: GenerationResult, response_time: float, total_time: float):

        answer_model: Dict[str, Any] = {
            "email_id": "test-id",
            "sender_email": email_from,
            "email_subject": subject,
            "email_body": body,
            "llm_prompt": prompt,
            "input_text_token_count": generation_result.input_text_token_count,
            "token_count": generation_result.token_count,
            "llm_completion_reason": generation_result.completion_reason,
            "llm_response": generation_result.output_text,
            "llm_text_generation_config": generation_result.text_generation_config,
            "llm_response_time_ms": int(response_time * 1000),
            "processing_status": "processed",
            "total_processing_time_ms": int(total_time * 1000),
            "error_message": None,
            "source_system": self._settings.source_system
        }

        self._database_service.create_answer(answer_model)
