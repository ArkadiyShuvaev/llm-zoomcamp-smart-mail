from dataclasses import dataclass, asdict
from typing import Dict
from uuid import UUID


@dataclass
class Project:
    """ Represents a project data. """

    id: UUID
    name: str

    @classmethod
    def create(cls, id: UUID, name: str) -> "Project":

        return cls(id=id, name=name)

    def to_mapping(self) -> Dict[str, str]:
        """
        Convert the Document instance to a dictionary.
        """
        return asdict(self)
