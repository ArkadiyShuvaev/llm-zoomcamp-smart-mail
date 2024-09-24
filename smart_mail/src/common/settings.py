import os
from typing import Any


class Settings:
    def __init__(self):
        self.elastic_search_url = self.get_env_variable("ELASTIC_SEARCH_URL")
        self.index_name = self.get_env_variable("INDEX_NAME")
        self.postgres_user = self.get_env_variable("POSTGRES_USER")
        self.postgres_password = self.get_env_variable("POSTGRES_PASSWORD")
        self.postgres_port = self.get_env_variable("POSTGRES_PORT")
        self.postgres_db = self.get_env_variable("POSTGRES_DB")
        self.source_system = self.get_env_variable("SOURCE_SYSTEM")
        self.postgres_host = self.get_env_variable("POSTGRES_HOST")
        self.embedding_model_name = self.get_env_variable("EMBEDDING_MODEL_NAME")

        self.use_local_llm = bool(self.get_env_variable("USE_LOCAL_LLM"))
        if self.use_local_llm is True:
            self.local_llm_url = self.get_env_variable("LOCAL_LLM_URL")
            self.local_llm_model_name = self.get_env_variable("LOCAL_LLM_MODEL_NAME")

    @staticmethod
    def get_env_variable(name: str) -> str:
        value = os.getenv(name)
        if value is None:
            raise EnvironmentError(f"Environment variable {name} is not set.")
        return value

    def to_dict(self) -> dict[str, Any]:
        return {
            "elastic_search_url": self.elastic_search_url,
            "index_name": self.index_name,
            "postgres_user": self.postgres_user,
            "postgres_password": self.postgres_password,
            "postgres_port": self.postgres_port,
            "postgres_db": self.postgres_db,
            "source_system": self.source_system,
            "postgres_host": self.postgres_host,
            "embedding_model_name": self.embedding_model_name,
            "use_local_llm": self.use_local_llm,
            "local_llm_url": self.local_llm_url if self.use_local_llm else "The 'use_local_llm' should be set to True to use this field.",
            "local_llm_model_name": self.local_llm_model_name if self.use_local_llm else "The 'use_local_llm' should be set to True to use this field.",
        }
