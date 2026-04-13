from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.services.user_service import create_user, approve_user
from app.db.session import get_db
from app.dependencies.auth import require_role

router = APIRouter()


# ---------------------------
# Create User (Executor)
# ---------------------------
@router.post("/")
def create_user_api(
    data: UserCreate,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Executor", "Maker"]))
):
    return create_user(db, data, user)


# ---------------------------
# Approve User (Executor 2)
# ---------------------------
@router.post("/{user_id}/approve")
def approve_user_api(
    user_id: str,
    db: Session = Depends(get_db),
    user=Depends(require_role(["Executor", "Maker"]))
):
    return approve_user(db, user_id, user)