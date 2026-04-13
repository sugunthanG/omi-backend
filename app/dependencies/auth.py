from fastapi import Depends, HTTPException, status, Header
from app.core.security import verify_token


# ------------------------
# Extract current user
# ------------------------
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header missing"
        )

    token = authorization.replace("Bearer ", "")
    payload = verify_token(token)

    return payload


# ------------------------
# Role Checker
# ------------------------
def require_role(allowed_roles: list):
    def role_checker(user=Depends(get_current_user)):
        user_role = user.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )

        return user

    return role_checker