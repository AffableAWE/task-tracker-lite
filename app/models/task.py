import enum

from sqlalchemy import Column, Integer, String, Text, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class TaskStatus(str, enum.Enum):
    todo = "Todo"
    doing = "Doing"
    done = "Done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, nullable=False)
    due_date = Column(Date, nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
