from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from common.model_base import ModelBase


class UserFeedbackTypeModel(ModelBase):

    __tablename__ = "user_feedback_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
