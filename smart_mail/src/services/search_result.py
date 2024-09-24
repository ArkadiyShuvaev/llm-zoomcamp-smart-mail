from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    Represents a search result.
    Attributes:
        score (float): The score of the search result.
        category (str): The category of the search result.
        question (str): The question of the search result.
        answer (str): The answer of the search result.
        document_id (str): The ID of the document.
        answer_instructions (str | None): The instructions for the answer, if any.
    """

    score: float
    category: str
    question: str
    answer: str
    document_id: str
    answer_instructions: str | None
