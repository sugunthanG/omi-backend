from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role
from app.models.approval import Approval


def create_user(db: Session, data, current_user):
    # Only Executor/Maker allowed
    role = db.query(Role).filter(Role.name == data.role).first()

    if not role:
        raise Exception("Invalid role")

    user = User(
        email=data.email,
        full_name=data.full_name,
        role_id=role.id,
        is_active=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create approval entry
    approval = Approval(
        entity_type="user",
        entity_id=user.id,
        requested_by=current_user["sub"],
        status="pending",
        step=1
    )

    db.add(approval)
    db.commit()

    return user


def approve_user(db: Session, user_id, current_user):
    approval = db.query(Approval).filter(
        Approval.entity_id == user_id,
        Approval.status == "pending"
    ).first()

    if not approval:
        raise Exception("No pending approval")

    # Prevent same executor approving
    if str(approval.requested_by) == current_user["sub"]:
        raise Exception("Cannot self-approve")

    if approval.step == 1:
        approval.step = 2
        approval.approved_by = current_user["sub"]

    elif approval.step == 2:
        approval.status = "approved"

        user = db.query(User).filter(User.id == user_id).first()
        user.is_active = True

    db.commit()

    return {"status": approval.status}