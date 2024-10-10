from dataclasses import dataclass
from typing import Any, Dict


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
        project_id (UUID | None): The GUID of the project, if exists.
        project_name (str | None): The name of the project, if exists.
    """

    score: float
    category: str
    question: str
    answer: str
    document_id: str
    answer_instructions: str | None
    project_id: str | None
    project_name: str | None
    authorization_id: str | None

    @classmethod
    def create(cls, score: float, doc: Dict[str, Any]) -> "SearchResult":

        answer_instructions_value = None
        answer_instructions: str | None = doc.get("answer_instructions")
        if answer_instructions is not None and answer_instructions.strip() != "":
            answer_instructions_value = answer_instructions

        project_name = doc.get("project_name") if not None else None

        result = cls(
            score,
            doc["category"],
            doc["question"],
            doc["answer"],
            doc["document_id"],
            answer_instructions_value,
            doc.get("project_id"),
            project_name,
            doc.get("authorization_id")
        )

        return result
