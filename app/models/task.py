from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.database import Base

class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(255), nullable=False)

    description = Column(Text)

    status = Column(String(50), default="todo")

    priority = Column(String(50), default="medium")

    due_date = Column(DateTime)

    created_by_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    assigned_to_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    updated_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship(
        "User",
        foreign_keys=[created_by_id]
    )

    assignee = relationship(
        "User",
        foreign_keys=[assigned_to_id]
    )