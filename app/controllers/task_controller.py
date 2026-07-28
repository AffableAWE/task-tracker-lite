from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskOut])
def list_my_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.list_my_tasks(db, current_user)


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.create_task(db, current_user, data)


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_service.update_task(db, task_id, current_user, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task_service.delete_task(db, task_id, current_user)
