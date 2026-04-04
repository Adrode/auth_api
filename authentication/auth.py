from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from database.database import get_db
from database import models

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

TIME_TO_EXPIRE = 15

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')

def hash_password(password: str) -> str:
  return password_hash.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
  return password_hash.verify(plain, hashed)

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  exp = datetime.now(timezone.utc) + timedelta(minutes=TIME_TO_EXPIRE)
  to_encode.update({'exp': exp})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
  token: str = Depends(oauth2_scheme),
  db: Session = Depends(get_db)
):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    email: str = payload.get('sub')
    if not email:
      raise HTTPException(
      status_code=401,
      detail='Not authorized',
      headers={'WWW-Authenticate': 'Bearer'}
    )
  except JWTError:
    raise HTTPException(
      status_code=401,
      detail='Not authorized',
      headers={'WWW-Authenticate': 'Bearer'}
    )
  
  user = db.query(models.User).where(models.User.email == email).first()

  if not user:
    raise HTTPException(
      status_code=401,
      detail='Not authorized',
      headers={'WWW-Authenticate': 'Bearer'}
    )
  
  return user