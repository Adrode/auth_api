from pydantic import BaseModel, EmailStr
import datetime

class CreateUser(BaseModel):
  email: EmailStr
  password: str

class User(BaseModel):
  email: EmailStr