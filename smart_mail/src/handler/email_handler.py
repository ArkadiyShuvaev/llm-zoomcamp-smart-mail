import time
import logging
from typing import Dict, Any

from common.settings import Settings
from services.database.database_service import DatabaseService
from services.generation.generation_result import GenerationResult
from services.generation.generation_service import GenerationService
from services.prompt_creator import PromptCreator
from services.retrieval_service import RetrievalService
from services.reciprocal_rank_fusion_service import ReciprocalRankFusionService


class EmailHandler:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        prompt_creator: PromptCreator,
        generation_service: GenerationService,
        database_service: DatabaseService,
        reciprocal_rank_fusion_service: ReciprocalRankFusionService,
        settings: Settings
    ) -> None:
        self._retrieval_service = retrieval_service
        self._prompt_creator = prompt_creator
        self._generation_service = generation_service
        self._database_service = database_service
        self.reciprocal_rank_fusion_service = reciprocal_rank_fusion_service
        self._settings = settings
        self._logger = logging.getLogger(__name__)

    def handle(self, email_from: str, subject: str, body: str) -> str:
        self._logger.info("Handling email from: %s, subject: %s", email_from, subject)

        start_time = time.time()
        # user_metadata = UserMetadata.create(email_from)

        retrieval_result = self._retrieval_service.search(body)

        reranked_search_results = self.reciprocal_rank_fusion_service.rerank(retrieval_result)
        used_results = reranked_search_results[:5]
        prompt = self._prompt_creator.create(body, used_results)

        start_llm_time = time.time()
        generation_result = self._generation_service.get_answer(prompt)
        end_llm_time = time.time()
        elapsed_llm_time = end_llm_time - start_llm_time

        end_time = time.time()
        elapsed_time = end_time - start_time

        created_entity = self._save_to_database(email_from, subject, body, prompt, generation_result, elapsed_llm_time, elapsed_time)
        self._logger.info(f"Created entity: {created_entity}")

        return str(generation_result.output_text)

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
