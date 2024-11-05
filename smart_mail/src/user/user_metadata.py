from dataclasses import asdict, dataclass
from typing import Dict
from data_loaders.email_loader import EmailLoader


@dataclass
class UserMetadata:
    exists: bool

    @classmethod
    def create(cls, email: str) -> "UserMetadata":
        exists = EmailLoader().exists(email)
        return cls(exists)

    def to_mapping(self) -> Dict[str, str | bool]:
        return asdict(self)
