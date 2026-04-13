from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    symbol = Column(String)
    signal = Column(String)
    entry = Column(Float)
    sl = Column(Float)
    tp = Column(Float)