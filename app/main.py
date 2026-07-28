from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.core.security import hash_password
from app.database import Base, engine, SessionLocal
from app.models import User, UserRole
from app.controllers import (
    auth_controller,
    category_controller,
    task_controller,
    admin_controller,
)


def seed_admin() -> None:
    """Create the default admin account if it doesn't exist yet."""
    db = SessionLocal()
    try:
        if not db.query(User).filter(User.email == settings.ADMIN_EMAIL).first():
            db.add(
                User(
                    name="Admin",
                    email=settings.ADMIN_EMAIL,
                    hashed_password=hash_password(settings.ADMIN_PASSWORD),
                    role=UserRole.admin,
                )
            )
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    yield


app = FastAPI(
    title="Task Tracker Lite",
    description="User authentication, roles & task management with categories",
    lifespan=lifespan,
)

app.include_router(auth_controller.router)
app.include_router(category_controller.router)
app.include_router(task_controller.router)
app.include_router(admin_controller.router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "docs": "/docs"}
