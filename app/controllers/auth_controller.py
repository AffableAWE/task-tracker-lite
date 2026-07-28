from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.deps import bearer_scheme, get_current_user, token_blacklist
from app.database import get_db
from app.models import User
from app.schemas.auth import RegisterIn, LoginIn, TokenOut, UserOut
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterIn, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.post("/login", response_model=TokenOut)
def login(data: LoginIn, db: Session = Depends(get_db)):
    token = auth_service.login_user(db, data)
    return TokenOut(access_token=token)


@router.post("/logout")
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: User = Depends(get_current_user),
):
    # get_current_user already validated the token; blacklist it now.
    token_blacklist.add(credentials.credentials)
    return {"detail": "Logged out successfully"}


@router.get("/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user
