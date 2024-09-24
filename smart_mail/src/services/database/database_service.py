import datetime
from typing import Any, List

from common.database_manager import DatabaseManager
from services.database.answer_model import AnswerModel
from sqlalchemy.orm import Session

from services.database.user_feedback_model import UserFeedbackModel
from services.database.user_feedback_type_model import UserFeedbackTypeModel
from sqlalchemy.orm import joinedload


class DatabaseService:
    def __init__(self, database_manager: DatabaseManager) -> None:
        self._database_manager = database_manager

    # Create a new record
    def create_answer(self, data: dict[str, Any]) -> AnswerModel:
        record = AnswerModel(**data)
        record.created_at = datetime.datetime.now()
        record.modified_at = datetime.datetime.now()

        with Session(self._database_manager.engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)

            return record

    def create_feedback(self, data: dict[str, Any]) -> UserFeedbackModel:
        record = UserFeedbackModel(**data)

        with Session(self._database_manager.engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)

            return record

    def get_answers(self, skip: int = 0, limit: int = 10) -> List[AnswerModel]:
        with Session(self._database_manager.engine) as session:
            return (
                session.query(AnswerModel)
                .options(joinedload(AnswerModel.user_feedback))
                .order_by(AnswerModel.modified_at.desc())
                .offset(skip)
                .limit(limit)
                .all()
            )

    def get_feedback_type_by_name(self, feedback_type_name: str = "negative") -> UserFeedbackTypeModel | None:
        with Session(self._database_manager.engine) as session:
            return session.query(UserFeedbackTypeModel).filter(UserFeedbackTypeModel.description == feedback_type_name).first()

    def get_answer_by_id(self, record_id: int) -> AnswerModel | None:
        with Session(self._database_manager.engine) as session:
            return (
                self._get_answer_by_id(record_id, session)
            )

    def update_answer(self, record_id: int, data: dict[str, Any]) -> AnswerModel | None:
        with Session(self._database_manager.engine) as session:
            record = self._get_answer_by_id(record_id, session)

            if record:
                record.modified_at = datetime.datetime.now()
                for key, value in data.items():
                    setattr(record, key, value)
                session.commit()
                session.refresh(record)

            return record

    def delete_record(self, record_id: int) -> AnswerModel | None:
        with Session(self._database_manager.engine) as session:
            record = self.get_answer_by_id(record_id)

            if record:
                session.delete(record)
                session.commit()

            return record

    def _get_answer_by_id(self, record_id: int, session: Session) -> AnswerModel | None:
        return (
            session.query(AnswerModel)
            .filter(AnswerModel.id == record_id)
            .options(joinedload(AnswerModel.user_feedback))
            .first()
        )
