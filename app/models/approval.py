from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    entity_type = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    requested_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    approved_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    status = Column(String, default="pending")
    step = Column(Integer, default=1)