from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password, create_access_token
from app.models import User
from app.schemas.auth import RegisterIn, LoginIn


def register_user(db: Session, data: RegisterIn) -> User:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: LoginIn) -> str:
    user = db.query(User).filter(User.email == data.email).first()
    if user is None or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return create_access_token(user.id)
