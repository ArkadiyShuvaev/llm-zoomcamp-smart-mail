from typing import List
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

from dtos.identified_project import IdentifiedProject


class ProjectIdentifierService:
    def __init__(self, project_names: List[str]):
        self._project_names: List[str] = project_names
        self._model_name = "sentence-transformers/distiluse-base-multilingual-cased-v1"
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        self._model = AutoModel.from_pretrained(self._model_name)

    def extract_project(self, input_text: str, similarity_threshold: float = 0.2) -> IdentifiedProject | None:
        # Get embeddings for the input text
        input_embedding = self._get_embeddings(input_text)

        # Get embeddings for each project name
        project_embeddings = [self._get_embeddings(project_name) for project_name in self._project_names]

        # Compute cosine similarities between input text and each project name
        similarities: List[float] = [cosine_similarity(input_embedding.unsqueeze(0), proj_emb.unsqueeze(0)).item() for proj_emb in project_embeddings]

        max_similarity_value: float = max(similarities)
        if max_similarity_value <= similarity_threshold:
            return None

        # Find the most similar project name
        best_match_index = similarities.index(max_similarity_value)
        best_project_name = self._project_names[best_match_index]

        return IdentifiedProject(name=best_project_name, similarity=max_similarity_value)

    # Tokenization function
    def _get_embeddings(self, text: str):
        inputs = self._tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self._model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()
