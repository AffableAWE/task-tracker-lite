from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas.category import CategoryIn


def _get_or_404(db: Session, category_id: int) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category


def list_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name).all()


def create_category(db: Session, data: CategoryIn) -> Category:
    if db.query(Category).filter(Category.name == data.name).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Category with this name already exists",
        )
    category = Category(name=data.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, data: CategoryIn) -> Category:
    category = _get_or_404(db, category_id)
    category.name = data.name
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = _get_or_404(db, category_id)
    # Detach tasks instead of deleting them
    for task in category.tasks:
        task.category_id = None
    db.delete(category)
    db.commit()
