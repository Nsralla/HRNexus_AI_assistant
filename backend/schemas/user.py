from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid

# User Registration
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    company_id: Optional[uuid.UUID] = None  # Optional: auto-create company if None

# User Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# User Response (without password)
class UserResponse(BaseModel):
    id: uuid.UUID
    company_id: uuid.UUID
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# JWT Token Response (with user data)
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# OAuth2 Token Response (Swagger compatible)
class OAuth2Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
