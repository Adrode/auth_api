from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
  __tablename__ = "users"
  id = Column(Integer, primary_key=True)
  email = Column(String, unique=True, nullable=False)
  hashed_password = Column(String, nullable=False)
  created_at = Column(Date, nullable=False)

  refresh_tokens = relationship('RefreshToken', back_populates='user', passive_deletes=True)

class RefreshToken(Base):
  __tablename__ = "refresh_tokens"
  id = Column(Integer, primary_key=True)
  hashed_token = Column(String, unique=True, nullable=False)
  user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
  expires_at = Column(Date, nullable=False)
  created_at = Column(Date, nullable=False)
  user_agent = Column(String)
  ip_address = Column(String)
  
  user = relationship('User', back_populates='refresh_tokens')