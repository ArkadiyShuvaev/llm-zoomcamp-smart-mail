from typing import Any, Dict, List
from uuid import UUID

from sentence_transformers import SentenceTransformer
from torch import Tensor
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

    SOURCE_FIELDS = ["score", "category", "question", "answer", "document_id",
                     "answer_instructions", "project_id", "authorization_id", "project_name"]

    def __init__(
        self,
        es_client: Elasticsearch,
        embedding_model: SentenceTransformer,
        settings: Settings,
    ) -> None:
        self.es_client = es_client
        self.embedding_model = embedding_model
        self.settings = settings

    def search(self,
               question: str,
               number_of_results: int = 20,
               vector_field_name: str = "vector_question_answer",
               customer_project_id: UUID | None = None,
               authorization_ids: List[str] | None = []) -> RetrievalResult:
        """
        Search for user_question in the retrieval service.

        Args:
            question (str): The question to search for.
            number_of_results (int, optional): The number of results to retrieve. Defaults to 10.
            vector_field_name (str, optional): The name of the field containing the vector embeddings. Defaults to "vector_question_answer".
            customer_project_id (str | None): A project id to filter the retrieval result. If the result does not have field 'project_id', the one is included.
            authorization_ids (List[str], optional): A list of authorization ids to filter the protected documents that the user has access to. Defaults to [].

        Returns:
            RetrievalResult: The retrieval result containing text_result_items and vector_result_items.
        """
        authorization_ids = authorization_ids or []

        # TODO: Move to Content Data preparer
        customer_project_id_upcased: str | None = str(customer_project_id) if customer_project_id is not None else None
        number_of_results_per_type = int(number_of_results / 2)

        vector_result = self._get_vector_search_result(question, number_of_results_per_type, vector_field_name, customer_project_id_upcased, authorization_ids)
        text_result = self._get_text_retrieval_result(question, number_of_results_per_type, customer_project_id_upcased, authorization_ids)

        # filtered_vector_result = self._filter_knn_results(vector_result, customer_project_id)

        return RetrievalResult(text_result_items=text_result, vector_result_items=vector_result)

    def _get_text_retrieval_result(self,
                                   user_question: str,
                                   number_of_results: int,
                                   customer_project_id: str | None,
                                   authorization_ids: List[str]) -> List[SearchResult]:

        text_query = self._create_text_query(user_question, self.settings.source_system, customer_project_id, authorization_ids)

        body: Dict[str, Any] = {
            "query": text_query,
            "size": number_of_results,
            "_source": self.SOURCE_FIELDS
        }
        text_response = self.es_client.search(index=self.settings.index_name, body=body)

        result: List[SearchResult] = []

        for hit in text_response["hits"]["hits"]:
            retrieval_result = self._create_search_result(hit)
            result.append(retrieval_result)

        return result

    def _get_vector_search_result(self,
                                  user_question: str,
                                  number_of_results: int,
                                  vector_field_name: str,
                                  customer_project_id: str | None,
                                  authorization_ids: List[str]) -> List[SearchResult]:

        query_vector = self.embedding_model.encode(user_question)

        knn_query = self._create_knn_query(vector_field_name, query_vector, number_of_results, self.settings.source_system, customer_project_id, authorization_ids)

        knn_response = self.es_client.search(
            index=self.settings.index_name,
            body={
                "knn": knn_query,
                "_source": self.SOURCE_FIELDS
            },
        )

        result: List[SearchResult] = []

        for hit in knn_response["hits"]["hits"]:
            retrieval_result = self._create_search_result(hit)
            result.append(retrieval_result)

        return result

    def _filter_knn_results(self, knn_results: List[SearchResult], customer_project_id: UUID | None) -> List[SearchResult]:
        """ Filter out items which project_id is not in the list of requested ids. """

        if customer_project_id is None:
            return knn_results

        results: List[SearchResult] = []

        for knn_result in knn_results:
            if knn_result.project_id is None:
                results.append(knn_result)
                continue

            if knn_result.project_id == customer_project_id:
                results.append(knn_result)

        return results

    def _create_search_result(self, hit: Dict[str, Any]) -> SearchResult:
        result = SearchResult.create(hit["_score"], hit["_source"])
        return result

    def _create_knn_query(
        self,
        vector_field_name: str,
        query_vector: Tensor,
        number_of_results: int,
        source_system: str,
        customer_project_id: str | None,
        authorization_ids: List[str] | None
    ) -> Dict[str, Any]:
        return {
            "field": vector_field_name,
            "query_vector": query_vector,
            "k": number_of_results,
            "num_candidates": 10000,
            "filter": self._create_filter_block(source_system, customer_project_id, authorization_ids)
        }

    def _create_text_query(
        self,
        user_question: str,
        source_system: str,
        customer_project_id: str | None,
        authorization_ids: List[str] | None
    ) -> Dict[str, Any]:
        return {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": user_question,
                        "fields": ["question^2", "answer^2", "category", "project_name"],
                        "type": "best_fields"
                    }
                },
                "filter": self._create_filter_block(source_system, customer_project_id, authorization_ids)
            }
        }

    def _create_filter_block(
        self,
        source_system: str,
        customer_project_id: str | None,
        authorization_ids: List[str] | None
    ) -> Dict[str, Any]:
        # Base query (KNN or text search) with a filter block
        base_query = {
            "bool": {
                "should": [
                    # Case 1: Public documents (no project_id, no authorization_id)
                    {"bool": {"must_not": {"exists": {"field": "project_id"}}}},
                ]
            }
        }

        # Case 2: Documents with project_id only
        if customer_project_id is not None:
            base_query["bool"]["should"].append(
                {
                    "bool": {
                        "must": [
                            {"exists": {"field": "project_id"}},
                            {"term": {"project_id": customer_project_id}},
                            {"bool": {"must_not": {"exists": {"field": "authorization_id"}}}}
                        ]
                    }
                }
            )

        # Case 3: Documents with both project_id and authorization_id
        if customer_project_id is not None and authorization_ids:
            base_query["bool"]["should"].append(
                {
                    "bool": {
                        "must": [
                            {"term": {"project_id": customer_project_id}},
                            {"terms": {"authorization_id": authorization_ids}}
                        ]
                    }
                }
            )

        # Optional filter: source_system
        base_filter = [{"term": {"source_system": source_system}}]
        
        # Dynamically add the boost functions only if the relevant fields are present
        functions = []

        # Boost Case 3 (highest boost)
        if customer_project_id is not None and authorization_ids:
            functions.append({
                "filter": {
                    "bool": {
                        "must": [
                            {"term": {"project_id": customer_project_id}},
                            {"terms": {"authorization_id": authorization_ids}}
                        ]
                    }
                },
                "weight": 5  # Increase rank for Case 3
            })

        # Boost Case 2 (lower boost than Case 3)
        if customer_project_id is not None:
            functions.append({
                "filter": {
                    "bool": {
                        "must": [
                            {"exists": {"field": "project_id"}},
                            {"term": {"project_id": customer_project_id}},
                            {"bool": {"must_not": {"exists": {"field": "authorization_id"}}}}
                        ]
                    }
                },
                "weight": 3  # Increase rank for Case 2
            })

        # Build the final boosted query only if there are boost functions defined
        if functions:
            boosted_query = {
                "function_score": {
                    "query": {
                        "bool": {
                            "must": base_filter,
                            "should": base_query["bool"]["should"],
                            "minimum_should_match": 1  # At least one condition must match
                        }
                    },
                    "functions": functions,
                    "boost_mode": "sum"  # Combine the base score with the boost weights
                }
            }
        else:
            # Fallback to the base query if no boost conditions are applicable
            boosted_query = {
                "bool": {
                    "must": base_filter,
                    "should": base_query["bool"]["should"],
                    "minimum_should_match": 1  # At least one condition must match
                }
            }

        return boosted_query
