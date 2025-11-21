from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from core.database import Base


class MessageFeedback(Base):
    __tablename__ = "message_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False, unique=True)
    rating = Column(Integer, nullable=False)  # 1 = thumbs up, -1 = thumbs down
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    message = relationship("Message", back_populates="feedback")

    def __repr__(self):
        return f"<MessageFeedback(id={self.id}, rating={self.rating})>"
