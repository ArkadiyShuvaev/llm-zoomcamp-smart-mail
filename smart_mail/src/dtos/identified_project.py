from dataclasses import dataclass


@dataclass
class IdentifiedProject:
    """Provides members for the project name identification feature"""
    name: str
    similarity: float
