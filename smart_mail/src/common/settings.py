import os
from typing import Any
import boto3
from boto3.session import Session


class Settings:
    def __init__(self):
        """
        Initializes the Settings object by loading environment variables and AWS configuration.

        Attributes:
            elastic_search_url (str): URL for the Elasticsearch instance.
            index_name (str): Name of the Elasticsearch index.
            postgres_user (str): Username for the PostgreSQL database.
            postgres_password (str): Password for the PostgreSQL database.
            postgres_port (str): Port number for the PostgreSQL database.
            postgres_db (str): Name of the PostgreSQL database.
            source_system (str): Identifier for the source system.
            postgres_host (str): Hostname for the PostgreSQL database.
            embedding_model_name (str): Name of the embedding model to use.
            use_local_llm (bool): Flag indicating whether to use a local LLM (Language Learning Model).
            local_llm_url (str, optional): URL for the local LLM API. Only set if USE_LOCAL_LLM is True.
            local_llm_model_name (str, optional): Name of the local LLM model. Only set if USE_LOCAL_LLM is True.
            aws_configuration_profile_name (str, optional): AWS configuration profile name. Only set if USE_LOCAL_LLM is False.
            aws_region_name (str, optional): AWS region name. Only set if USE_LOCAL_LLM is False.
            aws_model_name (str, optional): Name of the AWS model to use. Only set if USE_LOCAL_LLM is False.
        """

        self.elastic_search_url = self.get_env_variable("ELASTIC_SEARCH_URL")
        self.index_name = self.get_env_variable("INDEX_NAME")
        self.postgres_user = self.get_env_variable("POSTGRES_USER")
        self.postgres_password = self.get_env_variable("POSTGRES_PASSWORD")
        self.postgres_port = self.get_env_variable("POSTGRES_PORT")
        self.postgres_db = self.get_env_variable("POSTGRES_DB")
        self.source_system = self.get_env_variable("SOURCE_SYSTEM")
        self.postgres_host = self.get_env_variable("POSTGRES_HOST")
        self.embedding_model_name = self.get_env_variable("EMBEDDING_MODEL_NAME")

        use_local_llm_str = self.get_env_variable("USE_LOCAL_LLM")
        self.use_local_llm = use_local_llm_str.lower() in ("true", "1", "yes", "y")

        if self.use_local_llm is True:
            self.local_llm_url = self.get_env_variable("LOCAL_LLM_URL")
            self.local_llm_model_name = self.get_env_variable("LOCAL_LLM_MODEL_NAME")
            return

        self.aws_configuration_profile_name = self.get_env_variable("AWS_CONFIGURATION_PROFILE_NAME")
        session: Session = boto3.Session(profile_name=self.aws_configuration_profile_name)
        self.aws_region_name = session.region_name if session.region_name else self.get_env_variable("AWS_REGION_NAME")
        self.aws_model_name = self.get_env_variable("AWS_MODEL_NAME")

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
            "aws_configuration_profile_name": self.aws_configuration_profile_name if not self.use_local_llm else "The 'use_local_llm' should be set to False to use this field.",
            "aws_region_name": self.aws_region_name if not self.use_local_llm else "The 'use_local_llm' should be set to False to use this field.",
            "aws_model_name": self.aws_model_name if not self.use_local_llm else "The 'use_local_llm' should be set to False to use this field.",
        }
