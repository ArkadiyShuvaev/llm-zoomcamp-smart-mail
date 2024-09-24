from dataclasses import asdict, dataclass
from typing import Dict
from agents.email_agent import EmailAgent


@dataclass
class UserMetadata:
    exists: bool

    @classmethod
    def create(cls, email: str) -> "UserMetadata":
        exists = EmailAgent().exists(email)
        return cls(exists)

    def to_mapping(self) -> Dict[str, str | bool]:
        return asdict(self)
