from services.reciprocal_rank_fusion_service import ReciprocalRankFusionService
from services.retrieval_result import RetrievalResult
from services.search_result import SearchResult


def test_rerank():
    # Create the actual dataset
    text_result_items = [
        SearchResult(score=1.0, document_id="doc1", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.8, document_id="doc2", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.8, document_id="doc4", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None)
    ]

    vector_result_items = [
        SearchResult(score=0.9, document_id="doc2", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.7, document_id="doc3", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.7, document_id="doc1", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
    ]

    actual_dataset = RetrievalResult(
        text_result_items=text_result_items,
        vector_result_items=vector_result_items
    )

    # Create the expected dataset
    expected_result = [
        SearchResult(score=0.03252247488101534, document_id="doc2", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.032266458495966696, document_id="doc1", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.016129032258064516, document_id="doc3", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
        SearchResult(score=0.015873015873015872, document_id="doc4", category="unused_field", question="unused_field", answer="unused_field", answer_instructions=None),
    ]

    # Instantiate the service
    service = ReciprocalRankFusionService()

    # Perform the re-ranking
    actual_result = service.rerank(actual_dataset)

    # Assert the results
    assert actual_result == expected_result, f"Expected {expected_result}, but got {actual_result}"
