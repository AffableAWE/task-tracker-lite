from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models import Task, Category, User, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate


def _validate_category(db: Session, category_id: int | None) -> None:
    if category_id is None:
        return
    if not db.query(Category).filter(Category.id == category_id).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )


def _get_owned_task_or_404(db: Session, task_id: int, owner: User) -> Task:
    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.owner_id == owner.id)
        .first()
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    return task


def list_my_tasks(db: Session, owner: User) -> list[Task]:
    return (
        db.query(Task)
        .filter(Task.owner_id == owner.id)
        .order_by(Task.due_date)
        .all()
    )


def create_task(db: Session, owner: User, data: TaskCreate) -> Task:
    _validate_category(db, data.category_id)
    task = Task(**data.model_dump(), owner_id=owner.id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(db: Session, task_id: int, owner: User, data: TaskUpdate) -> Task:
    task = _get_owned_task_or_404(db, task_id, owner)
    changes = data.model_dump(exclude_unset=True)

    # Core business rule: status is frozen once the due date has passed.
    if "status" in changes and changes["status"] != task.status:
        if date.today() > task.due_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot change status: the task's due date has passed",
            )

    if "category_id" in changes:
        _validate_category(db, changes["category_id"])

    for field, value in changes.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, owner: User) -> None:
    task = _get_owned_task_or_404(db, task_id, owner)
    db.delete(task)
    db.commit()


def admin_list_tasks(
    db: Session,
    user_id: int | None = None,
    task_status: TaskStatus | None = None,
    due_before: date | None = None,
    due_after: date | None = None,
) -> list[Task]:
    """Admin dashboard: all tasks, filterable by user, status, due date range."""
    query = db.query(Task).options(joinedload(Task.owner))
    if user_id is not None:
        query = query.filter(Task.owner_id == user_id)
    if task_status is not None:
        query = query.filter(Task.status == task_status)
    if due_before is not None:
        query = query.filter(Task.due_date <= due_before)
    if due_after is not None:
        query = query.filter(Task.due_date >= due_after)
    return query.order_by(Task.due_date).all()
