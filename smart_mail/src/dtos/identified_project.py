from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class IdentifiedProject:
    """Provides members for the project name identification feature"""

    name: str
    id: UUID
    similarity: float
