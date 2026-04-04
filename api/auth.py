from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Annotated
from database import models
from authentication import auth
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
      hashed_password=auth.hash_password(data.password)
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
  
@router.post('/login')
def login(
  db: session_dependency,
  form_data: OAuth2PasswordRequestForm = Depends()
):
  user = db.query(models.User).where(models.User.email == form_data.username).first()

  if not user or not auth.verify_password(form_data.password, user.hashed_password):
    raise HTTPException(
      status_code=404,
      detail='Not found'
    )
  
  token = auth.create_access_token(data={'sub': user.email})
  return {'access_token': token, 'token_type': 'bearer'}