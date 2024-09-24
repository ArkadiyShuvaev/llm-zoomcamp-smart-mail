from common.model_base import ModelBase
from services.database.user_feedback_type_model import UserFeedbackTypeModel
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class UserFeedbackModel(ModelBase):

    __tablename__ = "user_feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserFeedbackTypeModel.id), nullable=False)
    feedback: Mapped[str] = mapped_column(String(800), nullable=True)
