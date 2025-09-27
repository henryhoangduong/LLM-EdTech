import json
from datetime import datetime

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from core.database import Base
from models.HenryDoc import HenryDoc


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class SQLDocument(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    data = Column(JSONB, nullable=False)
    chunks = relationship(
        "ChunkEmbedding", back_populates="documcSent", cascade="all, delete-orphan"
    )

    @classmethod
    def from_henrydoc(cls, doc: HenryDoc, user_id: str) -> "SQLDocument":
        return cls(
            id=doc.id,
            user_id=user_id,
            data=json.loads(json.dumps(doc.dict(), cls=DateTimeEncoder)),
        )

    def to_henrydoc(self) -> HenryDoc:
        """Convert to SimbaDoc"""
        return HenryDoc(**self.data)
