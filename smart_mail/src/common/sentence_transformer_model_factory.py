from common.settings import Settings
from sentence_transformers import SentenceTransformer


class SentenceTransformerModelFactory:
    def __init__(self, settings: Settings) -> None:
        self.model_name = settings.embedding_model_name

    def create_model(self) -> SentenceTransformer:
        # TODO: revision=4.7.0 (https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v1/resolve/main/config.json)
        return SentenceTransformer(self.model_name)
