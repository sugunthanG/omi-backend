from fastapi import APIRouter, Depends
from app.dependencies.auth import require_role

router = APIRouter()


@router.get("/maker-only")
def maker_route(user=Depends(require_role(["Maker"]))):
    return {
        "message": "Welcome Maker",
        "user": user
    }


@router.get("/executor-only")
def executor_route(user=Depends(require_role(["Executor", "Maker"]))):
    return {
        "message": "Executor access granted",
        "user": user
    }


@router.get("/user")
def user_route(user=Depends(require_role(["User", "Executor", "Maker"]))):
    return {
        "message": "User access granted",
        "user": user
    }