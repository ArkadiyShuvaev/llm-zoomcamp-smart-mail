import math
from services.retrieval_result import RetrievalResult
from services.search_result import SearchResult
from typing import Dict, List


class ReciprocalRankFusionService:
    """
    Reciprocal rank fusion service.
    This class represents a service for performing reciprocal rank fusion.
    It is used to combine the rankings of multiple search engines or recommendation systems into a single ranking.
    The fusion is based on the reciprocal ranks of the items in the rankings.
    See the following link to get more details https://www.elastic.co/guide/en/elasticsearch/reference/current/rrf.html to get more details.
    """

    def rerank(self, retrieval_result: RetrievalResult) -> List[SearchResult]:
        """
        Re-rank the search results using the reciprocal rank fusion algorithm.

        Parameters
        ----------
        retrieval_result : RetrievalResult
            The search result to be re-ranked.

        Returns
        -------
        SearchResult
            The re-ranked search result.
        """

        document_ids = self._get_document_ids(retrieval_result)

        if len(document_ids) == 0:
            return []

        reciprocal_ranks = self._get_reciprocal_ranks(retrieval_result, document_ids)
        return self._rerank_search_results(retrieval_result, reciprocal_ranks)

    def _rerank_search_results(self, retrieval_result: RetrievalResult, reciprocal_ranks: Dict[str, float]) -> List[SearchResult]:
        result: List[SearchResult] = []

        retrieval_result_as_list = retrieval_result.vector_result_items
        retrieval_result_as_list.extend(retrieval_result.text_result_items)

        ordered_rrf = sorted(reciprocal_ranks.items(), key=lambda x: x[1], reverse=True)

        for doc_id, rank in ordered_rrf:
            for item in retrieval_result_as_list:
                if item.document_id == doc_id:
                    search_result = SearchResult(
                        score=rank,
                        category=item.category,
                        question=item.question,
                        answer=item.answer,
                        document_id=item.document_id,
                        answer_instructions=item.answer_instructions,
                        project_id=item.project_id,
                        project_name=item.project_name,
                        authorization_id=item.authorization_id
                    )

                    result.append(search_result)
                    break

        return result

    def _get_reciprocal_ranks(self, retrieval_result: RetrievalResult, document_ids: set[str], k: int = 60) -> Dict[str, float]:
        result: Dict[str, float] = {}

        for document_id in document_ids:
            score = self._get_reciprocal_rank(retrieval_result, document_id, k)
            result[document_id] = score

        return result

    def _get_reciprocal_rank(self, retrieval_result: RetrievalResult, document_id: str, k: int) -> float:
        score = 0.0

        rank: float = self._get_document_rank(document_id, retrieval_result.text_result_items)
        score += 1.0 / (k + rank)
        rank = self._get_document_rank(document_id, retrieval_result.vector_result_items)
        score += 1.0 / (k + rank)
        return score

    def _get_document_rank(self, document_id: str, search_results: List[SearchResult]) -> float:
        for idx, doc in enumerate(search_results):
            if document_id is doc.document_id:
                return idx + 1

        return math.inf

    def _get_document_ids(self, retrieval_result: RetrievalResult) -> set[str]:
        document_ids: set[str] = set()

        for text_item in retrieval_result.text_result_items:
            document_ids.add(text_item.document_id)

        for vector_item in retrieval_result.vector_result_items:
            document_ids.add(vector_item.document_id)

        return document_ids
