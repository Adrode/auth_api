from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

TIME_TO_EXPIRE = 15

pwd_context = CryptContext(schemes=['bcrypt'])

print("schemes: ", pwd_context.schemes())
print("default scheme: ", pwd_context.default_scheme())

def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
  return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  exp = datetime.now() + timedelta(minutes=TIME_TO_EXPIRE)
  to_encode.update({'exp': exp})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)