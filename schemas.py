from pydantic import BaseModel, EmailStr
from datetime import datetime

class CreateUser(BaseModel):
  email: EmailStr
  password: str

class User(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime