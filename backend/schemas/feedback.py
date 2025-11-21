from pydantic import BaseModel
from datetime import datetime
import uuid

class FeedbackCreate(BaseModel):
    message_id: uuid.UUID
    rating: int  # 1 or -1

class FeedbackResponse(BaseModel):
    id: uuid.UUID
    message_id: uuid.UUID
    rating: int
    created_at: datetime

    class Config:
        from_attributes = True
