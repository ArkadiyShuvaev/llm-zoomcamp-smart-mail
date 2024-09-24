from dataclasses import dataclass


@dataclass
class SearchResult():
    score: float
    category: str
    question: str
    answer: str
    document_id: str
    answer_instructions: str | None
