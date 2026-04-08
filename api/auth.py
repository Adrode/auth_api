import hashlib
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import models
from authentication import short, long
from schemas import schemas
from database.database import get_db

router = APIRouter()

session_dependency = Annotated[Session, Depends(get_db)]

@router.post('/register', response_model=schemas.User)
def register(
  data: schemas.CreateUser,
  db: session_dependency
):
  try:
    user = models.User(
      email=data.email,
      hashed_password=short.hash_password(data.password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )
  
@router.post('/login', response_model=schemas.Token)
def login(
  db: session_dependency,
  form_data: OAuth2PasswordRequestForm = Depends()
):
  try:
    user = db.query(models.User).where(models.User.email == form_data.username).first()
    refresh_tokens = db.query(models.RefreshToken).where(models.RefreshToken.user_id == user.id).all()

    if not user or not short.verify_password(form_data.password, user.hashed_password):
      raise HTTPException(
        status_code=401,
        detail='Not authorized'
      )
    
    token = short.create_access_token(data={'sub': user.email})
    refresh_token = long.create_refresh_token()
    new_refresh_token = models.RefreshToken(
      hashed_token=refresh_token['hashed_token'],
      user_id=user.id,
      expires_at=refresh_token['expires_at']
    )
    
    if len(refresh_tokens) >= 5:
      oldest_refresh_token = db.query(models.RefreshToken).where(models.RefreshToken.user_id == user.id).order_by(models.RefreshToken.created_at.asc()).first()
      db.delete(oldest_refresh_token)
      
    db.add(new_refresh_token)
    db.commit()
    db.refresh(new_refresh_token)
  except IntegrityError:
    raise HTTPException(
      status_code=400,
      detail="Bad request"
    )

  return {'access_token': token, 'token_type': 'bearer', 'refresh_token': refresh_token['token']}

@router.post('/refresh')
def refresh(db: session_dependency, token: str):
  hashed = hashlib.sha256(token.encode()).hexdigest()

  old_refresh_token = db.query(models.RefreshToken).where(models.RefreshToken.hashed_token == hashed).first()

  if not old_refresh_token:
    raise HTTPException(
      status_code=404,
      detail='Not found'
    )
  
  db.delete(old_refresh_token)
  new_refresh_token = long.create_refresh_token()['hashed_token']