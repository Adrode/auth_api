from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUser(BaseModel):
  email: EmailStr
  password: str

class User(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

class Token(BaseModel):
  access_token: str
  token_type: str

class CreateRefreshToken(BaseModel):
  hashed_token: str
  user_id: int
  expires_at: datetime
  user_agent: str | None = None
  ip_address: str | None = None