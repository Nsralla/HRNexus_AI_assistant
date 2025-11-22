from pydantic import BaseModel
from datetime import datetime
import uuid

class ChatCreate(BaseModel):
    title: str = "New Conversation"

class ChatResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    company_id: uuid.UUID
    title: str
    created_at: datetime

    class Config:
        from_attributes = True

