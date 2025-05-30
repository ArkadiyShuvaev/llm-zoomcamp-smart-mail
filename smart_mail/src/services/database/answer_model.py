import datetime
from typing import Any
from sqlalchemy import DateTime, Integer, String, Text, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from common.model_base import ModelBase
from services.database.user_feedback_model import UserFeedbackModel


class AnswerModel(ModelBase):
    """
    AnswerModel represents a database model for storing information related to processed
    LLM (Language Model) responses based on incoming emails or other text inputs.

    Table: answer

    Columns:
    --------
    - id (int): Primary key, auto-incremented. Unique identifier for each record.
    - sender_email (VARCHAR(255)): Stores the sender's email address from which the input originated.
    - email_subject (VARCHAR(255)): Stores the subject of the email or message received.
    - email_body (Text): Stores the body content of the received email or message.
    - llm_prompt (Text): The prompt or query sent to the LLM for generating a response.
    - input_text_token_count (int): The count of tokens in the prompt sent to the LLM. Used for monitoring input complexity and LLM costs.
    - token_count (int): The count of tokens in the response generated by the LLM.
    - llm_completion_reason (VARCHAR(255)): Reason for LLM completion, e.g., 'max tokens reached', 'timeout', etc.
    - llm_text_generation_config (JSON): Configuration settings used for text generation by the LLM.
    - llm_response (Text): The response generated by the LLM based on the prompt.
    - llm_response_time_ms (int): Time taken (in milliseconds) by the LLM to generate the response. Useful for performance tracking.
    - processing_status (VARCHAR(50)): Tracks the status of the processing, e.g., 'pending', 'processed', or 'error'.
    - error_message (VARCHAR(255)): Logs any error message encountered during processing. Useful for debugging and error analysis.
    - source_system (VARCHAR(255)): Identifies the originating system or application for the record. Useful in multi-system integrations.
    - user_feedback_id (Integer): Feedback type provided by the user.
    - metadata (JSON): Stores additional context, structured data, or other relevant metadata associated with the record.
    - total_processing_time_ms (int): The total time spent processing the record, including the LLM response time.
    - created_at (TIMESTAMP): Automatically records the timestamp when the record is created. Useful for tracking when the data was logged.
    - modified_at (TIMESTAMP): Automatically updates the timestamp whenever the record is modified. Helps track data modifications over time.
    """

    __tablename__ = "answer"

    # Primary key, unique identifier
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Email fields
    email_id: Mapped[str] = mapped_column(String(255), nullable=False)  # Unique identifier for the email
    sender_email: Mapped[str] = mapped_column(String(255), nullable=False)  # Sender's email address
    email_subject: Mapped[str] = mapped_column(String(255), nullable=False)  # Subject of the email
    email_body: Mapped[str] = mapped_column(Text, nullable=False)  # Body of the email content

    # LLM interaction fields
    llm_prompt: Mapped[str | None] = mapped_column(Text, nullable=False)  # Prompt sent to the LLM
    input_text_token_count: Mapped[int | None] = mapped_column(Integer, nullable=False)  # Input token count
    token_count: Mapped[int | None] = mapped_column(Integer, nullable=False)  # Output token count
    llm_completion_reason: Mapped[str | None] = mapped_column(String(255), nullable=False)  # LLM completion reason
    llm_text_generation_config: Mapped[dict[str, int | float | str] | None] = mapped_column(JSON, nullable=False)  # Text generation configuration
    llm_response: Mapped[str | None] = mapped_column(Text, nullable=True)  # LLM generated response
    llm_response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=False)  # Response time in milliseconds

    # Processing and status fields
    processing_status: Mapped[str | None] = mapped_column(String(50), nullable=False)  # Status of the processing (e.g., processed, error)
    error_message: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Error message if any occurred

    # Additional context and feedback
    source_system: Mapped[str | None] = mapped_column(String(255), nullable=False)  # Originating system identifier

    user_feedback_id: Mapped[int | None] = mapped_column(Integer, ForeignKey(UserFeedbackModel.id), nullable=True)
    user_feedback = relationship("UserFeedbackModel", backref="answer")

    # Metadata and time tracking
    request_metadata: Mapped[dict[Any, Any] | None] = mapped_column(JSON, nullable=True)  # Additional structured information (JSON format)
    total_processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Time spent processing the record

    # Timestamps
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=False)  # Record creation timestamp
    modified_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=False)  # Record last updated timestamp
