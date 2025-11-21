from pydantic import BaseModel
from datetime import datetime
import uuid

class MessageCreate(BaseModel):
    chat_id: uuid.UUID
    content: str
    role: str = "user"  # user or assistant

class MessageResponse(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    user_id: uuid.UUID
    content: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True
