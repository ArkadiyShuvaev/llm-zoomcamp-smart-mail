import streamlit as st
from common.client_factory import ClientFactory
from common.emails import get_legitimate_emails, get_scammer_emails
from handler.email_handler import EmailHandler
from common.settings import Settings
from common.sentence_transformer_model_factory import (
    SentenceTransformerModelFactory as ModelFactory,
)

from services.database.database_service import DatabaseService
from services.prompt_creator import PromptCreator
from services.generation.aws_generation_service import AwsGenerationService
from services.reciprocal_rank_fusion_service import ReciprocalRankFusionService
from services.retrieval_service import RetrievalService


# Initialization
settings = Settings()
client_factory = ClientFactory(settings)
es_client = client_factory.create_elasticsearch_client()
model_factory = ModelFactory(settings)
embedding_model = model_factory.create_model()
retrieval_service = RetrievalService(es_client, embedding_model, settings)
generation_service = client_factory.create_generation_service()
database_manager = client_factory.create_database_manager()
database_service = DatabaseService(database_manager)
email_handler = EmailHandler(
    retrieval_service, PromptCreator(), generation_service, database_service, ReciprocalRankFusionService(), settings
)

database_manager.db_init()


# Predefined emails for the dropdown
emails = get_legitimate_emails()
emails.extend(get_scammer_emails())

# Main UI Components
with st.container(border=True):
    st.title("Email client")

    email_from = st.selectbox("Email From", emails) or ""
    subject = st.text_input("Subject") or ""
    body_control = st.text_area("Body") or ""

    # Send button
    if st.button("Send"):
        email_handler.handle(email_from, subject, body_control)
        st.success("Email sent!")
