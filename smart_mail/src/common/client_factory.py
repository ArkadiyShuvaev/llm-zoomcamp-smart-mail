from elasticsearch import Elasticsearch
import psycopg2
import boto3
from boto3.session import Session
from mypy_boto3_bedrock_runtime import BedrockRuntimeClient
from common.database_manager import DatabaseManager
from common.settings import Settings
from services.generation.generation_service import GenerationService
from services.generation.aws_generation_service import AwsGenerationService
from services.generation.ollama_generation_service import OllamaGenerationService


class ClientFactory:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def create_elasticsearch_client(self) -> Elasticsearch:
        return Elasticsearch(self._settings.elastic_search_url)

    def create_postgresql_connection(self):
        return psycopg2.connect(
            dbname=self._settings.postgres_db,
            user=self._settings.postgres_user,
            password=self._settings.postgres_password,
            host=self._settings.postgres_host,
            port=self._settings.postgres_port,
        )

    def create_database_manager(self) -> DatabaseManager:
        database_manager = DatabaseManager(self._settings)

        return database_manager

    def create_generation_service(self) -> GenerationService:
        if self._settings.use_local_llm:
            return OllamaGenerationService(self._settings)

        return AwsGenerationService(self._settings, self._create_bedrock_client())

    def _create_bedrock_client(self) -> BedrockRuntimeClient:
        session: Session = boto3.Session(profile_name=self._settings.aws_configuration_profile_name)

        bedrock_runtime: BedrockRuntimeClient = session.client(
            service_name="bedrock-runtime", region_name=self._settings.aws_region_name
        )

        return bedrock_runtime
