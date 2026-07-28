from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user, require_admin
from app.database import get_db
from app.models import User
from app.schemas.category import CategoryIn, CategoryOut
from app.services import category_service

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryOut])
def list_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Normal users can VIEW categories (they need to, to assign tasks),
    # but only admins can create/update/delete below.
    return category_service.list_categories(db)


@router.post("", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryIn,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return category_service.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryIn,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    return category_service.update_category(db, category_id, data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    category_service.delete_category(db, category_id)
