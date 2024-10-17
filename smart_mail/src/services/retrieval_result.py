from dataclasses import dataclass
from typing import List
from services.search_result import SearchResult


@dataclass
class RetrievalResult:
    """
    RetrievalResult class represents the result of a retrieval operation.

    Attributes:
        text_result_items (List[SearchResult]): A list of SearchResult objects representing the text-based retrieval results.
        vector_result_items (List[SearchResult]): A list of SearchResult objects representing the vector-based retrieval results.
    """
    text_result_items: List[SearchResult]
    vector_result_items: List[SearchResult]
