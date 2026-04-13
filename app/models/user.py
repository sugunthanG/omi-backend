from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    email = Column(String, unique=True, nullable=False)
    full_name = Column(String)

    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))

    is_active = Column(Boolean, default=False)