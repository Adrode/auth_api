from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from database.database import get_db
from database import models

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

TIME_TO_EXPIRE = 15

pwd_context = CryptContext(schemes=['bcrypt'])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

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

def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: Session = Depends(get_db)
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    email: str = payload.get('sub')
    if not id:
      raise HTTPException(
      status_code=404,
      detail='Not found'
    )
  except JWTError:
    raise HTTPException(
      status_code=404,
      detail='Not found'
    )
  
  user = db.query(models.User).where(models.User.email == email).first()

  if not user:
    raise HTTPException(
      status_code=404,
      detail='Not found'
    )
  
  return user