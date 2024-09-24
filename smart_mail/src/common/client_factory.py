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
        self.settings = settings

    def create_elasticsearch_client(self) -> Elasticsearch:
        return Elasticsearch(self.settings.elastic_search_url)

    def create_postgresql_connection(self):
        return psycopg2.connect(
            dbname=self.settings.postgres_db,
            user=self.settings.postgres_user,
            password=self.settings.postgres_password,
            host="localhost",  # Assuming localhost; adjust as needed
            port=self.settings.postgres_port,
        )

    def create_database_manager(self) -> DatabaseManager:
        database_manager = DatabaseManager(self.settings)

        return database_manager

    def create_generation_service(self) -> GenerationService:
        if self.settings.use_local_llm:
            return OllamaGenerationService(self.settings)

        return AwsGenerationService(self._create_bedrock_client())

    def _create_bedrock_client(self) -> BedrockRuntimeClient:
        session: Session = boto3.Session(profile_name="private")
        bedrock_runtime: BedrockRuntimeClient = session.client(
            # because of Amazon Titan Text Premier. The previous value: eu-central-1
            "bedrock-runtime", region_name="us-east-1"
        )

        return bedrock_runtime
