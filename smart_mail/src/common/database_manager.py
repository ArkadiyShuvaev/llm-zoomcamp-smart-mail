from urllib.parse import quote_plus
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from common.model_base import ModelBase
from common.settings import Settings
from services.database.user_feedback_type_model import UserFeedbackTypeModel


class DatabaseManager:
    def __init__(self, settings: Settings) -> None:
        encoded_password = quote_plus(settings.postgres_password)
        self.connection_string = f"postgresql://{settings.postgres_user}:{encoded_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
        self._engine = create_engine(self.connection_string, echo=True)

    @property
    def engine(self) -> Engine:
        return self._engine

    def db_init(self) -> None:

        ModelBase.metadata.create_all(bind=self.engine)

        with Session(self.engine) as session:
            # Check if the rows already exist
            existing_feedbacks = session.query(UserFeedbackTypeModel).filter(
                UserFeedbackTypeModel.description.in_(["neutral", "negative"])
            ).all()

            if existing_feedbacks:
                return

            feedback1 = UserFeedbackTypeModel(description="neutral")
            feedback2 = UserFeedbackTypeModel(description="negative")

            session.add_all([feedback1, feedback2])
            session.commit()
