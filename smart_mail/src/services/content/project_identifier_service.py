from typing import Sequence
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

from dtos.identified_project import IdentifiedProject

from dtos.project import Project
from services.content.text_preprocessor_service import TextPreprocessorService


class ProjectIdentifierService:
    def __init__(self, projects: Sequence[Project]):
        self._projects = projects

        preprocessed_projects = [ self._create_project(project) for project in projects ]
        self._sorted_projects_with_preprocessed_names = sorted(preprocessed_projects, key=lambda p: len(p.name), reverse=True)

        self._model_name = "sentence-transformers/distiluse-base-multilingual-cased-v1"
        self._tokenizer = AutoTokenizer.from_pretrained(self._model_name)
        self._model = AutoModel.from_pretrained(self._model_name)

        # Get embeddings for each project name
        self._project_embeddings = [self._get_embeddings(project.name) for project in self._projects]

    def extract_project(self, query: str, similarity_threshold: float = 0.5) -> IdentifiedProject | None:
        matched_projects = self.get_matched_projects(query)

        if matched_projects:
            project = matched_projects[0]
            confidence = 1  # Exact match, so confidence is 100%

            return IdentifiedProject(project.name, project.id, confidence)

        # Step 2: If no exact match, fall back to similarity matching
        project_match = self.extract_project_using_embeddings(query)
        confidence = (project_match.similarity + 1) / 2

        if confidence < similarity_threshold:
            return None

        return IdentifiedProject(project_match.name, project_match.id, confidence)

    def get_matched_projects(self, query: str) -> Sequence[Project]:
        query = TextPreprocessorService.preprocess_text(query)
        matched_projects = [project for project in self._sorted_projects_with_preprocessed_names if project.name in query]

        return matched_projects

    def extract_project_using_embeddings(self, input_text: str) -> IdentifiedProject:
        # Get embeddings for the input text
        input_text = input_text.replace("\n", " ").replace("\r", " ").replace("\t", " ").strip()

        input_embedding = self._get_embeddings(input_text)

        # Compute cosine similarities between input text and each project name
        similarities: Sequence[float] = [cosine_similarity(input_embedding.unsqueeze(0), proj_emb.unsqueeze(0)).item() for proj_emb in self._project_embeddings]

        max_similarity_value: float = max(similarities)

        # Find the most similar project name
        best_match_index = similarities.index(max_similarity_value)
        best_project = self._projects[best_match_index]

        return IdentifiedProject(best_project.name, best_project.id, max_similarity_value)

    # Tokenization function
    def _get_embeddings(self, text: str):
        inputs = self._tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self._model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze()

    def _create_project(self, project: Project) -> Project:
        project_name = TextPreprocessorService.preprocess_text(project.name)
        project = Project.create(project.id, project_name)
        return project
