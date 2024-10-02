from typing import List
from dtos.project import Project

from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity


class ProjectIdentifierService:
    def __init__(self, projects: List[Project]):
        self._projects: List[Project] = projects
        self._model_name = "sentence-transformers/distiluse-base-multilingual-cased-v1"
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        self._model = AutoModel.from_pretrained(self._model_name)

    def extract_project_name(self, input_text: str) -> str | None:
        # Get embeddings for the input text
        input_embedding = self._get_embeddings(input_text)

        # Get embeddings for each project name
        project_embeddings = [self._get_embeddings(project.name) for project in self._projects]

        # Compute cosine similarities between input text and each project name
        similarities: List[float] = [cosine_similarity(input_embedding.unsqueeze(0), proj_emb.unsqueeze(0)).item() for proj_emb in project_embeddings]

        max_similarity_value: float = max(similarities)
        if max_similarity_value <= 0.2:
            return None

        # Find the most similar project name
        best_match_index = similarities.index(max_similarity_value)
        best_project_name = self._projects[best_match_index].name

        return best_project_name

    # Tokenization function
    def _get_embeddings(self, text: str):
        inputs = self._tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self._model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()
