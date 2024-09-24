from dataclasses import dataclass
from typing import List

from services.search_result import SearchResult


@dataclass
class RetrievalResult():
    text_result_items: List[SearchResult]
    vector_result_items: List[SearchResult]
