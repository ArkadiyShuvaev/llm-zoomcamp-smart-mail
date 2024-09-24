from typing import Any, Dict, List

from sentence_transformers import SentenceTransformer
from common.settings import Settings
from services.search_result import SearchResult
from elasticsearch import Elasticsearch

from services.retrieval_result import RetrievalResult


class RetrievalService:
    """
    A service for retrieving search results from an Elasticsearch index using both text-based and vector-based search methods.

    This class provides methods to search for user queries in an Elasticsearch index, leveraging both traditional text search and vector search using embeddings.
    It integrates with Elasticsearch for text search and SentenceTransformer for generating query embeddings for vector search.

    Attributes:
        es_client (Elasticsearch): The Elasticsearch client used for querying the index.
        embedding_model (SentenceTransformer): The model used for generating embeddings for vector search.
        settings (Settings): Configuration settings for the retrieval service.
    """

    def __init__(
        self,
        es_client: Elasticsearch,
        embedding_model: SentenceTransformer,
        settings: Settings,
    ) -> None:
        self.es_client = es_client
        self.embedding_model = embedding_model
        self.settings = settings

    def search(self, user_question: str, number_of_results: int = 10, vector_field_name: str = "vector_question_answer") -> RetrievalResult:
        """
        Search for user_question in the retrieval service.

        Args:
            user_question (str): The question to search for.
            number_of_results (int, optional): The number of results to retrieve. Defaults to 10.
            vector_field_name (str, optional): The name of the field containing the vector embeddings. Defaults to "vector_question_answer".

        Returns:
            RetrievalResult: The retrieval result containing text_result_items and vector_result_items.
        """

        vector_result = self._get_vector_search_result(user_question, number_of_results, vector_field_name)
        text_result = self._get_text_retrieval_result(user_question, number_of_results)

        return RetrievalResult(text_result_items=text_result, vector_result_items=vector_result)

    def _get_text_retrieval_result(self, user_question: str, number_of_results: int) -> List[SearchResult]:
        text_query: Dict[str, Any] = {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": user_question,
                        "fields": ["question", "answer^3", "category"],
                        "type": "best_fields",
                        "boost": 0.5,
                    }
                },
                "filter": {"term": {"source_system": self.settings.source_system}},
            }
        }

        body: Dict[str, Any] = {
            "query": text_query,
            "size": number_of_results
        }
        text_response = self.es_client.search(index=self.settings.index_name, body=body)

        result: List[SearchResult] = []

        for hit in text_response["hits"]["hits"]:
            retrieval_result = self._create_search_result(hit)
            result.append(retrieval_result)

        return result

    def _get_vector_search_result(self, user_question: str, number_of_results: int, vector_field_name: str) -> List[SearchResult]:

        query_vector = self.embedding_model.encode(user_question)

        knn_query: Dict[str, Any] = {
            "field": vector_field_name,
            "query_vector": query_vector,
            "k": number_of_results,
            "num_candidates": 10000,
            "boost": 0.5,
            "filter": {"term": {"source_system": self.settings.source_system}},
        }

        knn_response = self.es_client.search(
            index=self.settings.index_name,
            body={
                "knn": knn_query,
                "_source": [
                    "source_system",
                    "category",
                    "question",
                    "answer",
                    "document_id",
                    "answer_instructions",
                ],
            },
        )

        result: List[SearchResult] = []

        for hit in knn_response["hits"]["hits"]:
            retrieval_result = self._create_search_result(hit)
            result.append(retrieval_result)

        return result

    def _create_search_result(self, hit: Dict[str, Any]) -> SearchResult:
        doc = hit["_source"]

        answer_instructions_value = None
        answer_instructions = doc.get("answer_instructions")
        if answer_instructions is not None or answer_instructions != "":
            answer_instructions_value = answer_instructions

        result = SearchResult(
            hit["_score"],
            doc["category"],
            doc["question"],
            doc["answer"],
            doc["document_id"],
            answer_instructions_value,
        )

        return result
