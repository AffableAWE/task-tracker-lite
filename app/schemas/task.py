from datetime import date

from pydantic import BaseModel, Field

from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus = TaskStatus.todo
    due_date: date
    category_id: int | None = None


class TaskUpdate(BaseModel):
    """All fields optional — send only what you want to change."""
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TaskStatus | None = None
    due_date: date | None = None
    category_id: int | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    due_date: date
    category_id: int | None

    class Config:
        from_attributes = True


class AdminTaskOut(TaskOut):
    """Dashboard view — includes who owns the task."""
    owner_id: int
    owner_name: str
    owner_email: str
