from typing import Any, Dict, List
import streamlit as st
import pandas as pd
from common.client_factory import ClientFactory
from handler.email_handler import EmailHandler
from common.settings import Settings
from common.sentence_transformer_model_factory import (
    SentenceTransformerModelFactory as ModelFactory,
)
from services.database.answer_model import AnswerModel
from services.database.database_service import DatabaseService
from services.prompt_creator import PromptCreator
from services.reciprocal_rank_fusion_service import ReciprocalRankFusionService
from services.retrieval_service import RetrievalService
from services.content.content_data_preparer import ContentDataPreparer


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
content_data_preparer = ContentDataPreparer()
email_handler = EmailHandler(
    retrieval_service, PromptCreator(), generation_service, database_service, ReciprocalRankFusionService(), content_data_preparer, settings
)

database_manager.db_init()


def get_user_feedback(answer: AnswerModel) -> str:
    if answer.user_feedback is None or answer.user_feedback.feedback is None:
        return ""

    length_limit = 15
    length = len(answer.user_feedback.feedback)
    if length <= length_limit:
        return answer.user_feedback.feedback

    return f"{answer.user_feedback.feedback[:length_limit]}...".strip()


def set_dislike(answer_id: int, feedback_value: str):
    feedback_type = database_service.get_feedback_type_by_name("negative")
    if feedback_type is None:
        raise Exception("Feedback type not found")

    feedback_dict: Dict[str, Any] = {
        "type_id": feedback_type.id,
        "feedback": feedback_value
    }
    feedback = database_service.create_feedback(feedback_dict)

    database_service.update_answer(answer_id, {
        "user_feedback_id": feedback.id
    })


def display_answer_by_id(answer_id: int):
    """
    Display the answer with the given ID.

    Parameters:
    - answer_id (int): The ID of the answer to display.

    Returns:
    None
    """
    answer: AnswerModel | None = database_service.get_answer_by_id(answer_id)

    with st.container():
        if answer is None:
            st.error("Answer not found")
            return

        st.markdown("**LLM Response:**")
        st.markdown(answer.llm_response, unsafe_allow_html=True)

        user_feedback = answer.user_feedback.feedback if answer.user_feedback else ""
        st.text_area("Feedback", user_feedback, key="current_feedback")

        def on_dislike():
            current_feedback = st.session_state.get("current_feedback", "")
            set_dislike(answer_id, current_feedback)

        st.button("I do not like it 👎", key=f"dislike_{answer_id}", help="Dislike", on_click=on_dislike)

        with st.expander("Question:"):
            st.markdown(f"**Sender Email:** {answer.sender_email}")
            st.markdown(f"**Subject:** {answer.email_subject}")
            st.markdown("**Email:**")
            st.markdown(answer.email_body)

        with st.expander("Technical details:"):
            st.markdown(f"**Source System:** {answer.source_system}")
            st.markdown(f"**Feedback:** {answer.user_feedback.feedback if answer.user_feedback else ''}")
            st.markdown(f"**Total Processing Time (ms):** {answer.total_processing_time_ms}")


def display_recent_answers():
    recent_answers = database_service.get_answers()

    if not recent_answers:
        st.info("No recent answers found.")
        return

    data: List[Dict[str, Any]] = [
        {
            "ID": answer.id,
            "": "👎" if answer.user_feedback_id is not None else "",
            "Email": answer.sender_email,
            "Subject": answer.email_subject,
            "Feedback": get_user_feedback(answer),
            "Modified": answer.modified_at,
        }
        for answer in recent_answers
    ]

    # Convert data to DataFrame
    df: pd.DataFrame = pd.DataFrame(data)

    # Display the table
    st.table(df.set_index("ID"))  # type: ignore


# Main UI Components
with st.container(border=True):
    st.title("Customer support client")

    answer_id_input = st.text_input("Enter Answer ID", "")
    if st.button("Read Answer"):
        if answer_id_input.isdigit():
            display_answer_by_id(int(answer_id_input))
        else:
            st.error("Please enter a valid numeric Answer ID")

    # Display recent answers
    display_recent_answers()
