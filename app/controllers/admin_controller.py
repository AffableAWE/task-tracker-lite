from datetime import date

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.deps import require_admin
from app.database import get_db
from app.models import User, TaskStatus
from app.schemas.task import AdminTaskOut
from app.services import task_service

router = APIRouter(prefix="/admin", tags=["Admin Dashboard"])


@router.get("/tasks", response_model=list[AdminTaskOut])
def dashboard(
    user_id: int | None = Query(default=None, description="Filter by user id"),
    status: TaskStatus | None = Query(default=None, description="Filter by task status"),
    due_before: date | None = Query(default=None, description="Tasks due on/before this date"),
    due_after: date | None = Query(default=None, description="Tasks due on/after this date"),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    tasks = task_service.admin_list_tasks(
        db,
        user_id=user_id,
        task_status=status,
        due_before=due_before,
        due_after=due_after,
    )
    return [
        AdminTaskOut(
            id=t.id,
            title=t.title,
            description=t.description,
            status=t.status,
            due_date=t.due_date,
            category_id=t.category_id,
            owner_id=t.owner.id,
            owner_name=t.owner.name,
            owner_email=t.owner.email,
        )
        for t in tasks
    ]
